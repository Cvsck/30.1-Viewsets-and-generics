from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), (~IsModerator)()]  # запрет модератору
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), (~IsModerator)()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
