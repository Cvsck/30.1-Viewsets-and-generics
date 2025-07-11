from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


# 🔹 ViewSet: удобный способ реализовать полный CRUD для курсов
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# 🔹 List + Create: вывод всех уроков и добавление нового
class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


# 🔹 Retrieve + Update + Delete: работа с конкретным уроком
class LessonRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
