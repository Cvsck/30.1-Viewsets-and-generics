import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from education.models import Course, Lesson, Subscription
from education.serializers import CourseSerializer, LessonSerializer
from education.validators import VideoURLValidator
from users.models import User


class EducationTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.owner = User.objects.create_user(
            email="owner@example.com", password="pass"
        )
        self.user = User.objects.create_user(email="user@example.com", password="pass")
        self.course = Course.objects.create(
            title="Курс", description="Описание курса", owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            title="Урок",
            video_url="https://www.youtube.com/watch?v=test",
            owner=self.owner,
            course=self.course,
        )

    # --- Views ---
    def test_course_view_get_queryset_user(self):
        # 🔀 Курс создаём от лица пользователя, а не owner
        course = Course.objects.create(
            title="Доступный курс", description="Для теста", owner=self.user
        )

        request = self.factory.get("/courses/")
        request.user = self.user

        from education.views import CourseViewSet

        view = CourseViewSet()
        view.request = request
        queryset = view.get_queryset()

        self.assertIn(course, queryset)

    # --- Course creation ---
    def test_course_create_authenticated(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("course-list")
        response = self.client.post(url, {"title": "Новый курс", "description": "Тест"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_create_unauthenticated(self):
        url = reverse("course-list")
        response = self.client.post(url, {"title": "Анонимный", "description": "..."})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_create_view(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("course-list")
        data = {"title": "Новый курс", "description": "Опис."}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Новый курс")

    def test_course_update_view(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.patch(url, {"title": "Обновлённый курс"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Обновлённый курс")

    def test_course_delete_view(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    def test_course_permission_denied_for_user(self):
        foreign_owner = User.objects.create_user(
            email="foreign@example.com", password="foreignpass"
        )
        foreign_course = Course.objects.create(
            title="Чужой", description="Тест", owner=foreign_owner
        )

        Subscription.objects.create(
            user=self.user, course=foreign_course
        )  # 👈 это даёт видимость

        self.client.force_authenticate(user=self.user)
        url = reverse("course-detail", args=[foreign_course.id])
        response = self.client.patch(url, {"title": "Попытка изменения"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Subscriptions ---
    def test_subscription_toggle(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("course-subscribe")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertIn(
            response.data["message"], ["подписка добавлена", "подписка удалена"]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- Serializers ---
    def test_course_serializer(self):
        request = self.factory.get("/")
        request.user = self.user
        serializer = CourseSerializer(
            instance=self.course, context={"request": request}
        )
        data = serializer.data
        self.assertEqual(data["title"], "Курс")
        self.assertEqual(data["description"], "Описание курса")
        self.assertIn("is_subscribed", data)
        self.assertIsInstance(data["is_subscribed"], bool)
        self.assertIn("lessons_count", data)
        self.assertEqual(data["lessons_count"], 1)

    def test_lesson_serializer_with_valid_url(self):
        data = {
            "title": "Тестовый урок",
            "video_url": "https://www.youtube.com/watch?v=abc123",
            "description": "Описание",
            "course": self.course.id,
        }
        serializer = LessonSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_lesson_serializer_with_invalid_url(self):
        data = {
            "title": "Неверный URL",
            "video_url": "https://vimeo.com/video123",
            "description": "Описание",
            "course": self.course.id,
        }
        serializer = LessonSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("video_url", serializer.errors)

    # --- Validators ---
    def test_video_url_validator_valid(self):
        validator = VideoURLValidator()
        try:
            validator("https://www.youtube.com/watch?v=test")
        except Exception:
            self.fail("Validator should not raise exception on valid URL")

    def test_video_url_validator_invalid(self):
        validator = VideoURLValidator()
        with self.assertRaises(Exception):
            validator("https://vimeo.com/123")
