from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url  # ✅ ДОБАВЛЕНО


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[validate_youtube_url]
    )  # ✅ ВАЛИДАЦИЯ YOUTUBE

    class Meta:
        model = Lesson
        fields = ["id", "title", "course", "description", "video_url"]
        read_only_fields = ["id"]


class FullCourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()  # ✅ ПОДПИСКА

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):  # ✅ МЕТОД ПОДПИСКИ
        user = self.context.get("request").user
        if user and user.is_authenticated:
            return Subscription.objects.filter(user=user, course=instance).exists()
        return False

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]
        read_only_fields = ["id", "lessons_count", "lessons", "is_subscribed"]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()  # ✅ ПОДПИСКА

    @staticmethod
    def get_lessons_count(instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):  # ✅ МЕТОД ПОДПИСКИ
        user = self.context.get("request").user
        if user and user.is_authenticated:
            return Subscription.objects.filter(user=user, course=instance).exists()
        return False

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons_count", "is_subscribed"]
        read_only_fields = ["id", "lessons_count", "is_subscribed"]
