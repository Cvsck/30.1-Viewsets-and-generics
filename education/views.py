from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import StandardPagination  # ✅ ПАГИНАЦИЯ
from .serializers import CourseSerializer, LessonSerializer


# ✅ КУРСЫ — CRUD + Подписка + Пагинация
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardPagination  # ✅ ПАГИНАЦИЯ

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["retrieve", "update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(Q(owner=user) | Q(subscription__user=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ✅ УРОКИ — список и создание
class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardPagination  # ✅ ПАГИНАЦИЯ

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):  # ✅ ОГРАНИЧЕНИЕ ВИДИМОСТИ
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ✅ УРОКИ — чтение, обновление, удаление
class LessonRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


# ✅ ПОДПИСКА НА КУРСЫ
class CourseSubscribeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        sub_qs = Subscription.objects.filter(user=user, course=course)

        if sub_qs.exists():
            sub_qs.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "подписка добавлена"

        return Response({"message": message})
