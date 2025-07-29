from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import VideoURLValidator


# ✅ Уроки — сериализатор с валидацией ссылки
class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[VideoURLValidator()]  # проверка HTTPS-ссылки на видео
    )

    class Meta:
        model = Lesson
        fields = ["id", "title", "course", "description", "video_url"]
        read_only_fields = ["id"]


# ✅ Курс + список уроков — полная детализация
class FullCourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

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

    def get_lessons_count(self, instance: Course) -> int:
        return instance.lessons.count()

    def get_is_subscribed(self, instance: Course) -> bool:
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            return Subscription.objects.filter(user=user, course=instance).exists()
        return False


# ✅ Курс без уроков — упрощённый вариант для списка
class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons_count", "is_subscribed"]
        read_only_fields = ["id", "lessons_count", "is_subscribed"]

    @staticmethod
    def get_lessons_count(instance: Course) -> int:
        return instance.lessons.count()

    def get_is_subscribed(self, instance: Course) -> bool:
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            return Subscription.objects.filter(user=user, course=instance).exists()
        return False


# ✅ Подписка на курс — для CourseSubscribeAPIView
class CourseSubscribeSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate_course_id(self, value):
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("Курс с таким ID не найден.")
        return value
