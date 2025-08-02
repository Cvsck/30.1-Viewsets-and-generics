from django.contrib import admin

from .models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_staff", "is_superuser", "avatar")
    search_fields = ("email",)
    list_filter = ("is_staff", "is_superuser")
    ordering = ("email",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "amount", "method", "course", "lesson")
    list_filter = ("method", "course", "lesson", "date")
    search_fields = ("user__email",)
    ordering = ("-date",)
