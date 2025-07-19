from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


# ✅ КУРСЫ — VIEWSET
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                IsAuthenticated,
                ~IsModerator,
            ]  # запрет модератору создавать
        elif self.action == "destroy":
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]  # только владелец может удалить
        elif self.action in ["retrieve", "update", "partial_update"]:
            permission_classes = [
                IsAuthenticated,
                IsModerator | IsOwner,
            ]  # оба могут редактировать
        else:
            permission_classes = [IsAuthenticated]  # list — только авторизованным
        return [permission() for permission in permission_classes]

    def get_queryset(self):  # ДОБАВЛЕНО — фильтрация по owner
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ✅ УРОКИ — СПИСОК И СОЗДАНИЕ
class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [
                IsAuthenticated,
                ~IsModerator,
            ]  # запрет модератору на создание
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):  # фильтрация по owner
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# УРОКИ — ЧТЕНИЕ / ОБНОВЛЕНИЕ / УДАЛЕНИЕ
class LessonRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]  # удалять может только владелец
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
