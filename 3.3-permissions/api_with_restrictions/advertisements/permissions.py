from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnlyForDelete(BasePermission):
    """
    Разрешение, которое:
    - Разрешает чтение всем (SAFE_METHODS),
    - Разрешает изменение и удаление владельцу объекта или администратору.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.creator == request.user or request.user.is_staff

