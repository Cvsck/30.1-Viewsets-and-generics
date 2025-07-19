from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import Course, Lesson


# 🔹 Кастомный менеджер пользователя
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        extra_fields.setdefault(
            "is_active", True
        )  # ✅ Устанавливаем активность по умолчанию
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault(
            "is_active", True
        )  # ✅ Убедимся, что суперюзер тоже активен

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")

        return self.create_user(email=email, password=password, **extra_fields)


# 🔹 Кастомная модель пользователя
class User(AbstractUser):
    username = None  # ❌ Убираем username — авторизация по email
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# 🔹 Модель платежей
class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("card", "Перевод на счёт"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"{self.user.email} — {self.amount}₽ — {self.method}"
