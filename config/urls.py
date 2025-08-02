from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path("admin/", admin.site.urls),
    # ✅ JWT-эндпоинты
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ✅ Swagger-документация
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="schema"
    ),  # генерация OpenAPI-схемы
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),  # интерфейс Swagger UI
    # ✅ Эндпоинты приложений
    path("api/users/", include("users.urls")),
    path("api/education/", include("education.urls")),
]

# ✅ Статика и медиа в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
