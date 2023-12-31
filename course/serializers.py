from rest_framework import serializers

from course.models import Course, Lesson, Payment, Subscription
#from course.services import get_payment
from course.validators import LinkVideoValidator


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    #amount = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)
    last_payment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_last_payment(self, instance):
        if instance.payment.all().first():
            return instance.payment.all().first().payment
        return 0


class CourseSerializer(serializers.ModelSerializer):
    last_payment = serializers.FloatField(source='payment.all.first.payment', read_only=True)
    lesson = LessonSerializer(source='lessons', many=True, read_only=True)
    payment = PaymentSerializer(many=True, read_only=True)
    subscribe = serializers.SerializerMethodField(read_only=True)
    count_lesson = serializers.SerializerMethodField(read_only=True)

    def get_count_lesson(self, instance):
        return instance.lessons.count()

    def get_subscribe(self, instance):
        request = self.context.get('request')
        if instance.subscribe.filter(user=request.user).exists():
            item = instance.subscribe.filter(user=request.user)
            return item[0].is_subscribe
        return False

    class Meta:
        model = Course
        fields = '__all__'


class LessonPaymentSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class LessonCreateSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkVideoValidator(field='link_video')]

    def create(self, validated_data):
        if validated_data.get('payment'):
            print(validated_data)
            payment = validated_data.pop('payment')
            lesson_item = Lesson.objects.create(**validated_data)
            for m in payment:
                Payment.objects.create(**m, lesson=lesson_item)

            return lesson_item
        return validated_data


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
