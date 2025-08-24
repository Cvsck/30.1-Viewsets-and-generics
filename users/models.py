from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import Course, Lesson


# рџ”№ РљР°СЃС‚РѕРјРЅС‹Р№ РјРµРЅРµРґР¶РµСЂ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email РѕР±СЏР·Р°С‚РµР»РµРЅ")
        email = self.normalize_email(email)
        extra_fields.setdefault(
            "is_active", True
        )  # вњ… РЈСЃС‚Р°РЅР°РІР»РёРІР°РµРј Р°РєС‚РёРІРЅРѕСЃС‚СЊ РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault(
            "is_active", True
        )  # вњ… РЈР±РµРґРёРјСЃСЏ, С‡С‚Рѕ СЃСѓРїРµСЂСЋР·РµСЂ С‚РѕР¶Рµ Р°РєС‚РёРІРµРЅ

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "РЎСѓРїРµСЂРїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РґРѕР»Р¶РµРЅ РёРјРµС‚СЊ is_staff=True"
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "РЎСѓРїРµСЂРїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РґРѕР»Р¶РµРЅ РёРјРµС‚СЊ is_superuser=True"
            )

        return self.create_user(email=email, password=password, **extra_fields)


# рџ”№ РљР°СЃС‚РѕРјРЅР°СЏ РјРѕРґРµР»СЊ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ
class User(AbstractUser):
    username = None  # вќЊ РЈР±РёСЂР°РµРј username вЂ” Р°РІС‚РѕСЂРёР·Р°С†РёСЏ РїРѕ email
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# рџ”№ РњРѕРґРµР»СЊ РїР»Р°С‚РµР¶РµР№
class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "РќР°Р»РёС‡РЅС‹Рµ"),
        ("card", "РџРµСЂРµРІРѕРґ РЅР° СЃС‡С‘С‚"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    stripe_product_id = models.CharField(max_length=255, blank=True)
    stripe_price_id = models.CharField(max_length=255, blank=True)
    stripe_session_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.email} вЂ” {self.amount}в‚Ѕ вЂ” {self.method}"
