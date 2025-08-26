from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (PaymentViewSet, RegisterAPIView, UserDetailView,
                    UserListCreateView, UserViewSet, payment_cancel,
                    payment_success)

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)
router.register(r"user-set", UserViewSet)

urlpatterns = [
    # Р СѓС‡РЅС‹Рµ РјР°СЂС€СЂСѓС‚С‹ РґР»СЏ РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # Р РµРіРёСЃС‚СЂР°С†РёСЏ
    path("register/", RegisterAPIView.as_view(), name="register"),
    # JWT-Р°РІС‚РѕСЂРёР·Р°С†РёСЏ
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ViewSet РґРѕСЃС‚СѓРїРµРЅ РїРѕ /api/user-set/
    path("", include(router.urls)),
    path("payment/success/", payment_success, name="payment_success"),
    path("payment/cancel/", payment_cancel, name="payment_cancel"),
]
