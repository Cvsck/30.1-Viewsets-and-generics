from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        is_mod = request.user.groups.filter(name="moderators").exists()
        print("IsModerator =", is_mod)
        return is_mod


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "owner") and obj.owner == request.user
