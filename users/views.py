from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema

from users.permissions import IsModerator, IsOwner, IsModeratorOrOwner
from .models import Payment
from .serializers import PaymentSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию о себе",
        description="Возвращает профиль текущего пользователя. Используется, например, для отображения личного кабинета.",
    ),
    post=extend_schema(
        summary="Создать пользователя (не используется во фронте)",
        description="Позволяет создать пользователя. Обычно недоступно напрямую на фронте.",
    ),
)
class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@extend_schema_view(
    get=extend_schema(
        summary="Получить подробную информацию о себе",
        description="Возвращает расширенный профиль текущего пользователя.",
    ),
    put=extend_schema(
        summary="Обновить свой профиль",
        description="Позволяет полностью обновить личные данные пользователя.",
    ),
    patch=extend_schema(
        summary="Частично обновить профиль",
        description="Обновление отдельных полей профиля пользователя.",
    ),
    delete=extend_schema(
        summary="Удалить аккаунт",
        description="Удаляет профиль текущего пользователя.",
    ),
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@extend_schema(
    summary="Регистрация нового пользователя",
    description="Открытая точка регистрации. Позволяет создать новый аккаунт.",
)
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    list=extend_schema(
        summary="Список всех пользователей",
        description="Позволяет модератору просматривать всех пользователей.",
    ),
    retrieve=extend_schema(
        summary="Получить пользователя по ID",
        description="Возвращает профиль конкретного пользователя. Доступно модератору.",
    ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        summary="Получить список платежей",
        description="Возвращает все платежи, доступные текущему пользователю. Модераторы видят всё, обычные — только свои.",
    ),
    create=extend_schema(
        summary="Создание нового платежа",
        description="Пользователь может создать платеж за курс или урок.",
    ),
    retrieve=extend_schema(
        summary="Получить платеж по ID",
        description="Возвращает информацию о конкретном платеже. Доступен владельцу или модератору.",
    ),
    update=extend_schema(
        summary="Обновление платежа",
        description="Позволяет обновить данные платежа.",
    ),
    destroy=extend_schema(
        summary="Удаление платежа",
        description="Удаляет платеж, если вы — владелец. Модераторы не могут удалять.",
    ),
)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["date"]

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated(), ~IsModerator()]
        elif self.action in ["update", "partial_update", "retrieve"]:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        return [IsAuthenticated()]
