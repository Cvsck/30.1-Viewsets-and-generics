from django.urls import reverse
from rest_framework.test import APITestCase

from education.models import Course, Lesson, Subscription
from users.models import User


class EducationTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com", password="pass"
        )
        self.user = User.objects.create_user(email="user@example.com", password="pass")
        self.course = Course.objects.create(
            title="Курс", description="...", owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            title="Урок",
            video_url="https://www.youtube.com/watch?v=test",
            owner=self.owner,
            course=self.course,
        )

    def test_course_create(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("course-list")
        response = self.client.post(url, {"title": "Новый курс", "description": "..."})
        self.assertEqual(response.status_code, 201)

    def test_subscription_toggle(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("course-subscribe")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertIn(
            response.data["message"], ["подписка добавлена", "подписка удалена"]
        )
