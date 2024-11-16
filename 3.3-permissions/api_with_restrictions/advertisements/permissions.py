from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsOwnerForDelete(BasePermission):
    """
    Разрешение, позволяющее удалять объект только его владельцу.
    """

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
