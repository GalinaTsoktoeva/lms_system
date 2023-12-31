import stripe
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from course.models import Course, Lesson, Payment, Subscription
from course.paginators import CoursePaginator
from course.permissions import IsOwner, IsModerator
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, \
    LessonPaymentSerializer, LessonCreateSerializer, SubscribeSerializer, PaymentCreateSerializer
from course.services import get_lesson_or_course, get_email
from course.tasks import send_update_course


class CourseViewSet(viewsets.ModelViewSet):

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            new_course = serializer.save()
            new_course.owner = self.request.user
            new_course.save()

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        subscrions = Subscription.objects.filter(user=request.user)
        emails = get_email(subscrions)
        send_update_course(emails)
        return super().update(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner|IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        #print(request.data.get('payment'))
        prod = request.data.get('payment')
        product = get_lesson_or_course(prod.get('lesson'), prod.get('course'))

        stripe.api_key = settings.PAY_API_KEY

        response = stripe.PaymentIntent.create(
            amount=prod.get('payment'),
            currency="rub",
            automatic_payment_methods={"enabled": True},
        )
        stripe.PaymentIntent.confirm(
            response.id,
            payment_method='pm_card_visa',
        )
        user = self.request.user
        payment_id = response.id
        data = {
            "stripe_payment_id": payment_id,
            "user": user,
            "status": response.status,
            "stripe_payment_url": response.url
        }
        #print(response)
        serializer = self.get_serializer(data=data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class LessonPaymentListAPIView(generics.ListAPIView):
     queryset = Payment.objects.filter(lesson__isnull=False)
     serializer_class = LessonPaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date_payment', )


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer