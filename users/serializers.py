from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Payment

User = (
    get_user_model()
)  # вњ… РџРѕР»СѓС‡Р°РµРј С‚РµРєСѓС‰СѓСЋ РјРѕРґРµР»СЊ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ РёР· settings.AUTH_USER_MODEL


# рџ”№ РЎРµСЂРёР°Р»РёР·Р°С‚РѕСЂ РґР»СЏ РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# рџ”№ РЎРµСЂРёР°Р»РёР·Р°С‚РѕСЂ РґР»СЏ РїР»Р°С‚РµР¶РµР№
class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        fields = "__all__"


# рџ”№ РЎРµСЂРёР°Р»РёР·Р°С‚РѕСЂ СЂРµРіРёСЃС‚СЂР°С†РёРё
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]  # вњ… username СѓРґР°Р»С‘РЅ

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data.get("email", ""),
            password=validated_data.get("password", ""),
        )
