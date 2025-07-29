from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema
from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import StandardPagination
from .serializers import CourseSerializer, LessonSerializer, CourseSubscribeSerializer


# ✅ КУРСЫ — CRUD + Подписка + Пагинация
@extend_schema(tags=["Courses"])
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

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
@extend_schema(tags=["Lessons"])
class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ✅ УРОКИ — чтение, обновление, удаление
@extend_schema(tags=["Lessons"])
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


# ✅ ПОДПИСКА НА КУРСЫ — исправленная для Swagger
@extend_schema(
    tags=["Courses"],
    summary="Оформить или отменить подписку на курс",
    request=CourseSubscribeSerializer,
    responses={200: CourseSubscribeSerializer},
)
class CourseSubscribeAPIView(GenericAPIView):
    serializer_class = CourseSubscribeSerializer
    permission_classes = [IsAuthenticated]

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

        serializer = self.get_serializer(data={"course_id": course.id})
        serializer.is_valid()  # Только для показа в Swagger
        return Response(
            {"message": message, "course_id": course.id}, status=status.HTTP_200_OK
        )
