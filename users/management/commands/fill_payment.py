from django.core.management import BaseCommand
from django.utils import timezone

from course.models import Course, Lesson, Payment
from users.models import User

from django.contrib.auth.hashers import make_password


class Command(BaseCommand):

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def handle(self, *args, **options):
        user_list = [
            {'first_name': 'Ivan', 'last_name': 'Ivanov', 'email': 'test7@sky.pro', 'password': make_password('12345')},
            {'first_name': 'Petr', 'last_name': 'Petrov', 'email': 'test6@sky.pro', 'password': make_password('12345')},
            {'first_name': 'Serg', 'last_name': 'Sergeev', 'email': 'test3@sky.pro', 'password': make_password('12345')},
            {'first_name': 'Olegka', 'last_name': 'Olegov', 'email': 'test4@sky.pro', 'password': make_password('12345')},
            {'first_name': 'Igor', 'last_name': 'Igorev', 'email': 'test5@sky.pro', 'password': make_password('12345')},
        ]
        user_for_create = []

        for user in user_list:
            user_for_create.append(
                User(**user)
            )

        User.objects.bulk_create(user_for_create)

        course_list = [
            {'pk': 1, 'name': 'Python', 'description': 'Начнем изучать Python и станем крутыми программистами'},
            {'pk': 2, 'name': 'Java', 'description': 'Начнем изучать Java и станем крутыми программистами'},
            {'pk': 3, 'name': 'Тестирование', 'description': 'Начнем изучать Тестирование и станем крутыми тестировщиками'}
        ]
        course_for_create = []

        for course in course_list:
            course_for_create.append(
                Course(**course)
            )
        Course.objects.bulk_create(course_for_create)

        lesson_list = [
            {'pk': 1, 'name': 'ООП', 'description': 'Обьектно-ориентированное программирование', 'course': Course.objects.get(name='Python')},
            {'pk': 2, 'name': 'База данных', 'description': 'Изучим базы данных', 'course': Course.objects.get(name='Python')},
            {'pk': 3, 'name': 'Django', 'description': 'как писать сайты на фрейморке Django', 'course': Course.objects.get(name='Python')},
            {'pk': 4, 'name': 'ООП', 'description': 'Обьектно-ориентированное программирование', 'course': Course.objects.get(name='Java')},
            {'pk': 5, 'name': 'База данных', 'description': 'Изучим базы данных', 'course': Course.objects.get(name='Java')},
            {'pk': 6, 'name': 'Doker', 'description': 'Doker', 'course': Course.objects.get(name='Java')},
            {'pk': 7, 'name': 'auto testy', 'description': 'auto testy', 'course': Course.objects.get(name='Тестирование')},
            {'pk': 8, 'name': 'Ручное тестирование', 'description': 'изучим мануальное тестирование', 'course': Course.objects.get(name='Тестирование')},
            {'pk': 9, 'name': 'UNIT тесты', 'description': 'UNIT тесты', 'course': Course.objects.get(name='Тестирование')},
        ]
        lesson_for_create = []

        for lesson in lesson_list:
            lesson_for_create.append(
                Lesson(**lesson)
            )
        Lesson.objects.bulk_create(lesson_for_create)

        payment_list = [
            {'user': User.objects.get(first_name='Ivan'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=1), 'lesson': Lesson.objects.get(pk=6), 'payment': 1234.3, 'payment_method': 1},
            {'user': User.objects.get(first_name='Petr'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=2), 'lesson': Lesson.objects.get(pk=4, course=Course.objects.get(name='Java')), 'payment': 123.3, 'payment_method': 2},
            {'user': User.objects.get(first_name='Serg'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=3), 'lesson': Lesson.objects.get(pk=8, course=Course.objects.get(name='Тестирование')), 'payment': 34.3, 'payment_method': 1},
            {'user': User.objects.get(first_name='Olegka'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=1), 'lesson': Lesson.objects.get(pk=3, course=Course.objects.get(name='Python')), 'payment': 234.3, 'payment_method': 2},
            {'user': User.objects.get(first_name='Olegka'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=3), 'lesson': Lesson.objects.get(pk=8, course=Course.objects.get(name='Тестирование')), 'payment': 123.3, 'payment_method': 1},
            {'user': User.objects.get(first_name='Ivan'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=1), 'lesson': Lesson.objects.get(pk=2, course=Course.objects.get(name='Python')), 'payment': 1000.3, 'payment_method': 2},
            {'user': User.objects.get(first_name='Petr'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=2), 'lesson': Lesson.objects.get(pk=6, course=Course.objects.get(name='Java')), 'payment': 1200.3, 'payment_method': 1},
            {'user': User.objects.get(first_name='Serg'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=3), 'lesson': Lesson.objects.get(pk=9, course=Course.objects.get(name='Тестирование')), 'payment': 12.0, 'payment_method': 1},
            {'user': User.objects.get(first_name='Olegka'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=2), 'lesson': Lesson.objects.get(pk=5, course=Course.objects.get(pk=2)), 'payment': 934.3, 'payment_method': 2},
            {'user': User.objects.get(first_name='Igor'), 'date_payment': timezone.now(), 'course': Course.objects.get(pk=3), 'lesson': Lesson.objects.get(pk=7, course=Course.objects.get(name='Тестирование')), 'payment': 9034.3, 'payment_method': 1},
        ]
        payment_for_create = []

        for payment in payment_list:
            payment_for_create.append(
                Payment(**payment)
            )
        Payment.objects.bulk_create(payment_for_create)