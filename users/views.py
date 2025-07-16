# users/views.py
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from users.permissions import IsModerator, IsNotModerator
from .models import Payment
from .serializers import UserSerializer, RegisterSerializer, PaymentSerializer

User = get_user_model()


# 🔹 Список + создание пользователей — только своих
class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Только текущий пользователь видит себя
        return User.objects.filter(id=self.request.user.id)


# 🔹 Работа с одним пользователем — можно редактировать себя
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Только текущий пользователь имеет доступ
        return User.objects.filter(id=self.request.user.id)


# 🔹 ViewSet для платежей с ограничениями на роли
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["date"]

    def get_permissions(self):
        # Явно запрещаем модераторам создавать/удалять
        if self.action in ["create", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


# 🔹 Регистрация нового пользователя
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# 🔹 ReadOnly ViewSet — можно добавить фильтрацию по роли
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
