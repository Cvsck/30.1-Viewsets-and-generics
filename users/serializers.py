from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Payment

User = (
    get_user_model()
)  # ✅ Получаем текущую модель пользователя из settings.AUTH_USER_MODEL


# 🔹 Сериализатор для пользователей
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# 🔹 Сериализатор для платежей
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


# 🔹 Сериализатор регистрации
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]  # ✅ username удалён

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data.get("email", ""),
            password=validated_data.get("password", ""),
        )
