from django.core.management import BaseCommand
from django.utils import timezone

from course.models import Course, Lesson, Payment
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_list = [
            {'first_name': 'Ivan', 'last_name': 'Ivanov', 'email': 'galinatsok@gmail.com'},
            {'first_name': 'Petr', 'last_name': 'Petrov', 'email': 'test6@sky.pro'},
            {'first_name': 'Serg', 'last_name': 'Sergeev', 'email': 'test3@sky.pro'},
            {'first_name': 'Olegka', 'last_name': 'Olegov', 'email': 'test4@sky.pro'},
            {'first_name': 'Igor', 'last_name': 'Igorev', 'email': 'test5@sky.pro'},
        ]
        user_for_create = []

        for user in user_list:
            user_for_create.append(
                User(**user)
            )

        #User.objects.bulk_create(user_for_create)

        course_list = [
            {'name': 'Python', 'description': 'Начнем изучать Python и станем крутыми программистами'},
            {'name': 'Java', 'description': 'Начнем изучать Java и станем крутыми программистами'},
            {'name': 'Тестирование', 'description': 'Начнем изучать Тестирование и станем крутыми тестировщиками'}
        ]
        course_for_create = []

        for course in course_list:
            course_for_create.append(
                Course(**course)
            )
        #Course.objects.bulk_create(course_for_create)

        lesson_list = [
            {'name': 'ООП', 'description': 'Обьектно-ориентированное программирование', 'course': Course.objects.get(name='Python')},
            {'name': 'База данных', 'description': 'Изучим базы данных', 'course': Course.objects.get(name='Python')},
            {'name': 'Django', 'description': 'как писать сайты на фрейморке Django', 'course': Course.objects.get(name='Python')},
            {'name': 'ООП', 'description': 'Обьектно-ориентированное программирование', 'course': Course.objects.get(name='Java')},
            {'name': 'База данных', 'description': 'Изучим базы данных', 'course': Course.objects.get(name='Java')},
            {'name': 'Doker', 'description': 'Doker', 'course': Course.objects.get(name='Java')},
            {'name': 'auto testy', 'description': 'auto testy', 'course': Course.objects.get(name='Тестирование')},
            {'name': 'Ручное тестирование', 'description': 'изучим мануальное тестирование', 'course': Course.objects.get(name='Тестирование')},
            {'name': 'UNIT тесты', 'description': 'UNIT тесты', 'course': Course.objects.get(name='Тестирование')},
        ]
        lesson_for_create = []

        for lesson in lesson_list:
            lesson_for_create.append(
                Lesson(**lesson)
            )
        #Lesson.objects.bulk_create(lesson_for_create)

        payment_list = [
            {'user': User.objects.get(first_name='Ivan'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Python'), 'lesson': Lesson.objects.get(name='Doker'), 'payment': 1234.3, 'payment_method': 1},
            {'user': User.objects.get(first_name='Petr'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Java'), 'lesson': Lesson.objects.get(name='ООП', course=Course.objects.get(name='Java')), 'payment': 123.3, 'payment_method': 2},
            {'user': User.objects.get(first_name='Serg'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Тестирование'), 'lesson': Lesson.objects.get(name='Ручное тестирование', course=Course.objects.get(name='Тестирование')), 'payment': 34.3, 'payment_method': 1},
            {'user': User.objects.get(first_name='Olegka'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Python'), 'lesson': Lesson.objects.get(name="Django", course=Course.objects.get(name='Python')), 'payment': 234.3, 'payment_method': 2},
            {'user': User.objects.get(first_name='Olegka'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Тестирование'), 'lesson': Lesson.objects.get(name='Ручное тестирование', course=Course.objects.get(name='Тестирование')), 'payment': 123.3, 'payment_method': 1},
            {'user': User.objects.get(first_name='Ivan'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Python'), 'lesson': Lesson.objects.get(name='База данных', course=Course.objects.get(name='Python')), 'payment': 1000.3, 'payment_method': 2},
            {'user': User.objects.get(first_name='Petr'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Java'), 'lesson': Lesson.objects.get(name='Doker', course=Course.objects.get(name='Java')), 'payment': 1200.3, 'payment_method': 1},
            {'user': User.objects.get(first_name='Serg'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Тестирование'), 'lesson': Lesson.objects.get(name='UNIT тесты', course=Course.objects.get(name='Тестирование')), 'payment': 12.0, 'payment_method': 1},
            {'user': User.objects.get(first_name='Olegka'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Python'), 'lesson': Lesson.objects.get(name='База данных', course=Course.objects.get(name='Python')), 'payment': 934.3, 'payment_method': 2},
            {'user': User.objects.get(first_name='Igor'), 'date_payment': timezone.now(), 'course': Course.objects.get(name='Тестирование'), 'lesson': Lesson.objects.get(name='auto testy', course=Course.objects.get(name='Тестирование')), 'payment': 9034.3, 'payment_method': 1},
        ]
        payment_for_create = []

        for payment in payment_list:
            payment_for_create.append(
                Payment(**payment)
            )
        Payment.objects.bulk_create(payment_for_create)