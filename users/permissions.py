from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    РџСЂРѕРІРµСЂСЏРµС‚, СЃРѕСЃС‚РѕРёС‚ Р»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РІ РіСЂСѓРїРїРµ 'moderators'.

    вњ… РџРѕРґРґРµСЂР¶РёРІР°РµС‚ РёРЅРІРµСЂСЃРёСЋ С‡РµСЂРµР· '~IsModerator()'.
    РСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РЅР° СѓСЂРѕРІРЅРµ has_permission.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="moderators").exists()
        )

    def __invert__(self):
        # Р’РѕР·РІСЂР°С‰Р°РµС‚ Permission, РѕС‚СЂРёС†Р°СЋС‰РёР№ РїСЂРёРЅР°РґР»РµР¶РЅРѕСЃС‚СЊ Рє РјРѕРґРµСЂР°С‚РѕСЂР°Рј
        class NotModerator(BasePermission):
            def has_permission(inner_self, request, view):
                return not IsModerator().has_permission(request, view)

        return NotModerator()


class IsOwner(BasePermission):
    """
    РџСЂРѕРІРµСЂСЏРµС‚, СЏРІР»СЏРµС‚СЃСЏ Р»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РІР»Р°РґРµР»СЊС†РµРј РѕР±СЉРµРєС‚Р°.

    вњ… РСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РЅР° СѓСЂРѕРІРЅРµ РѕР±СЉРµРєС‚Р° (retrieve/update/delete).
    """

    def has_object_permission(self, request, view, obj):
        return bool(hasattr(obj, "owner") and obj.owner == request.user)


class IsModeratorOrOwner(BasePermission):
    """
    вњ… РћР±СЉРµРґРёРЅС‘РЅРЅР°СЏ Р»РѕРіРёРєР° РґРѕСЃС‚СѓРїР°:
    СЂР°Р·СЂРµС€РµРЅРѕ, РµСЃР»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ вЂ” РјРѕРґРµСЂР°С‚РѕСЂ РёР»Рё РІР»Р°РґРµР»РµС† РѕР±СЉРµРєС‚Р°.
    """

    def has_permission(self, request, view):
        return IsModerator().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return IsModerator().has_permission(
            request, view
        ) or IsOwner().has_object_permission(request, view, obj)
