from django.contrib.auth import get_user_model
from django.http import (HttpResponse,  # вњ… РґРѕР±Р°РІР»РµРЅ РёРјРїРѕСЂС‚
                         JsonResponse)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permissions import IsModerator, IsModeratorOrOwner, IsOwner

from .models import Payment
from .serializers import PaymentSerializer, RegisterSerializer, UserSerializer
from .stripe_service import (create_checkout_session, create_stripe_price,
                             create_stripe_product)

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        summary="РџРѕР»СѓС‡РёС‚СЊ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ СЃРµР±Рµ",
        description="Р’РѕР·РІСЂР°С‰Р°РµС‚ РїСЂРѕС„РёР»СЊ С‚РµРєСѓС‰РµРіРѕ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ РґР»СЏ Р»РёС‡РЅРѕРіРѕ РєР°Р±РёРЅРµС‚Р°.",
    ),
    post=extend_schema(
        summary="РЎРѕР·РґР°С‚СЊ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ",
        description="РЎРѕР·РґР°РЅРёРµ РЅРѕРІРѕРіРѕ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ (РІ РѕСЃРЅРѕРІРЅРѕРј РґР»СЏ Р°РґРјРёРЅРєРё РёР»Рё РѕС‚Р»Р°РґРєРё).",
    ),
)
class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@extend_schema_view(
    get=extend_schema(summary="РњРѕР№ РїСЂРѕС„РёР»СЊ"),
    put=extend_schema(summary="РћР±РЅРѕРІРёС‚СЊ РїСЂРѕС„РёР»СЊ"),
    patch=extend_schema(summary="Р§Р°СЃС‚РёС‡РЅРѕ РѕР±РЅРѕРІРёС‚СЊ РїСЂРѕС„РёР»СЊ"),
    delete=extend_schema(summary="РЈРґР°Р»РёС‚СЊ Р°РєРєР°СѓРЅС‚"),
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@extend_schema(
    summary="Р РµРіРёСЃС‚СЂР°С†РёСЏ",
    description="РЎРѕР·РґР°С‘С‚ РЅРѕРІРѕРіРѕ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ С‡РµСЂРµР· РѕС‚РєСЂС‹С‚СѓСЋ С‚РѕС‡РєСѓ.",
)
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    list=extend_schema(summary="РЎРїРёСЃРѕРє РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№"),
    retrieve=extend_schema(summary="РџСЂРѕС„РёР»СЊ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ РїРѕ ID"),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        summary="РњРѕРё РїР»Р°С‚РµР¶Рё РёР»Рё РІСЃРµ (РґР»СЏ РјРѕРґРµСЂР°С‚РѕСЂР°)"
    ),
    create=extend_schema(summary="РЎРѕР·РґР°С‚СЊ РїР»Р°С‚РµР¶ Рё Stripe-СЃРµСЃСЃРёСЋ"),
    retrieve=extend_schema(summary="РџРѕР»СѓС‡РёС‚СЊ РїР»Р°С‚РµР¶ РїРѕ ID"),
    update=extend_schema(summary="РћР±РЅРѕРІРёС‚СЊ РїР»Р°С‚РµР¶"),
    destroy=extend_schema(summary="РЈРґР°Р»РёС‚СЊ РїР»Р°С‚РµР¶"),
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
        )  # Stripe С‚СЂРµР±СѓРµС‚ РІ РєРѕРїРµР№РєР°С…
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


# вњ… РЎС‚СЂР°РЅРёС†С‹ СѓСЃРїРµС…Р°/РѕС‚РјРµРЅС‹ РґР»СЏ Stripe
def payment_success(request):
    return JsonResponse(
        {"status": "success", "message": "РџР»Р°С‚С‘Р¶ РїСЂРѕС€С‘Р» СѓСЃРїРµС€РЅРѕ вњ…"}
    )


def payment_cancel(request):
    return JsonResponse(
        {
            "status": "cancelled",
            "message": "вќЊ РћРїР»Р°С‚Р° РѕС‚РјРµРЅРµРЅР° РёР»Рё РЅРµ СѓРґР°Р»Р°СЃСЊ.",
        }
    )
