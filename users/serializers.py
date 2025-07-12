from rest_framework import serializers
from .models import User
from rest_framework import serializers
from .models import Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# users/serializers.py


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
