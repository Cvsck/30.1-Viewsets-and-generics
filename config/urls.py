from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    # вњ… JWT-СЌРЅРґРїРѕРёРЅС‚С‹
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # вњ… Swagger-РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="schema"
    ),  # РіРµРЅРµСЂР°С†РёСЏ OpenAPI-СЃС…РµРјС‹
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),  # РёРЅС‚РµСЂС„РµР№СЃ Swagger UI
    # вњ… Р­РЅРґРїРѕРёРЅС‚С‹ РїСЂРёР»РѕР¶РµРЅРёР№
    path("api/users/", include("users.urls")),
    path("api/education/", include("education.urls")),
    path("", lambda request: HttpResponse("It works!")),
]

# вњ… РЎС‚Р°С‚РёРєР° Рё РјРµРґРёР° РІ СЂРµР¶РёРјРµ DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
