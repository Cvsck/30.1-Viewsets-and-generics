from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import payment_success, payment_cancel

from .views import (
    PaymentViewSet,
    RegisterAPIView,
    UserDetailView,
    UserListCreateView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)
router.register(r"user-set", UserViewSet)

urlpatterns = [
    # Ручные маршруты для пользователей
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # Регистрация
    path("register/", RegisterAPIView.as_view(), name="register"),
    # JWT-авторизация
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ViewSet доступен по /api/user-set/
    path("", include(router.urls)),
    path("payment/success/", payment_success, name="payment_success"),
    path("payment/cancel/", payment_cancel, name="payment_cancel"),
]
