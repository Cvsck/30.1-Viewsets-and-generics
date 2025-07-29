from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.http import HttpResponse, JsonResponse  # ✅ добавлен импорт

from users.permissions import IsModerator, IsOwner, IsModeratorOrOwner
from .models import Payment
from .serializers import PaymentSerializer, RegisterSerializer, UserSerializer
from .stripe_service import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
)

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию о себе",
        description="Возвращает профиль текущего пользователя для личного кабинета.",
    ),
    post=extend_schema(
        summary="Создать пользователя",
        description="Создание нового пользователя (в основном для админки или отладки).",
    ),
)
class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@extend_schema_view(
    get=extend_schema(summary="Мой профиль"),
    put=extend_schema(summary="Обновить профиль"),
    patch=extend_schema(summary="Частично обновить профиль"),
    delete=extend_schema(summary="Удалить аккаунт"),
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@extend_schema(
    summary="Регистрация",
    description="Создаёт нового пользователя через открытую точку.",
)
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    list=extend_schema(summary="Список пользователей"),
    retrieve=extend_schema(summary="Профиль пользователя по ID"),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="Мои платежи или все (для модератора)"),
    create=extend_schema(summary="Создать платеж и Stripe-сессию"),
    retrieve=extend_schema(summary="Получить платеж по ID"),
    update=extend_schema(summary="Обновить платеж"),
    destroy=extend_schema(summary="Удалить платеж"),
)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["date"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), ~IsModerator()]
        elif self.action in ["destroy"]:
            return [IsAuthenticated(), IsOwner()]
        elif self.action in ["retrieve", "update", "partial_update"]:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.validated_data.get("course")
        user = self.request.user

        product_id = create_stripe_product(name=course.title)
        price_id = create_stripe_price(
            product_id, amount=int(course.price * 100)
        )  # Stripe требует в копейках
        session_url = create_checkout_session(
            price_id=price_id,
            success_url="http://127.0.0.1:8000/api/users/payment/success/",
            cancel_url="http://127.0.0.1:8000/api/users/payment/cancel/",
        )

        serializer.save(
            user=user,
            stripe_product_id=product_id,
            stripe_price_id=price_id,
            stripe_session_url=session_url,
        )


# ✅ Страницы успеха/отмены для Stripe
def payment_success(request):
    return JsonResponse({"status": "success", "message": "Платёж прошёл успешно ✅"})


def payment_cancel(request):
    return JsonResponse(
        {"status": "cancelled", "message": "❌ Оплата отменена или не удалась."}
    )
