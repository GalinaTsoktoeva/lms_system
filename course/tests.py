from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com',
        )
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(
            name='test course',
            description='test course description',
        )

        self.lesson = Lesson.objects.create(
            name='test',
            description='test description',
            link_video='https://www.youtube.com',
            owner=self.user,
            course=self.course,
        )

    def test_create_lesson(self):

        """Тестирование создания урока"""
        data = {
            'name': 'test',
            'description': 'test description',
            'link_video': 'https://www.youtube.com',
            'course': self.course.pk,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            path='/lesson/create/', data=data,
        )
        print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Lesson.objects.all().exists(),
            {'name': 'test', 'img': None, 'description': 'test description', 'link_video': 'https://www.youtube.com',
             'course': 1, 'owner': 1}
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/lesson/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        print(response.json().get("results"))
        self.assertEqual(
            response.json().get("results"),
            [{'id': 1, 'name': 'test', 'img': None,'link_video': 'https://www.youtube.com','course': 1, 'owner':1, 'description': 'test description', 'payment': [], 'last_payment': 0}]
        )

    def test_lesson_retrieve(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/lesson/{self.lesson.pk}/')

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('name'), 'test')
        self.assertEqual(response.get('description'), 'test description')
        self.assertEqual(response.get('img'), None)
        self.assertEqual(response.get('link_video'), 'https://www.youtube.com')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'updated test',
            'description': 'updated test description',
        }

        response = self.client.put(
            path=f'/lesson/update/{self.lesson.pk}/', data=data,
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('name'), 'updated test')
        self.assertEqual(response.get('description'), 'updated test description')
        self.assertEqual(response.get('img'), None)
        self.assertEqual(response.get('link_video'), 'https://www.youtube.com')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/lesson/delete/{self.lesson.pk}/',
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()

