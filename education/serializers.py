from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "course", "description", "video_url"]
        read_only_fields = ["id"]


class FullCourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons_count", "lessons"]
        read_only_fields = ["id", "lessons_count", "lessons"]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons_count"]
        read_only_fields = ["id", "lessons_count"]
