from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверяет, состоит ли пользователь в группе 'moderators'.

    ✅ Поддерживает инверсию через '~IsModerator()'.
    Используется на уровне has_permission.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="moderators").exists()
        )

    def __invert__(self):
        # Возвращает Permission, отрицающий принадлежность к модераторам
        class NotModerator(BasePermission):
            def has_permission(inner_self, request, view):
                return not IsModerator().has_permission(request, view)

        return NotModerator()


class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта.

    ✅ Используется на уровне объекта (retrieve/update/delete).
    """

    def has_object_permission(self, request, view, obj):
        return bool(hasattr(obj, "owner") and obj.owner == request.user)


class IsModeratorOrOwner(BasePermission):
    """
    ✅ Объединённая логика доступа:
    разрешено, если пользователь — модератор или владелец объекта.
    """

    def has_permission(self, request, view):
        return IsModerator().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return IsModerator().has_permission(
            request, view
        ) or IsOwner().has_object_permission(request, view, obj)
