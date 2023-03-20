from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ только администратору или только для чтения."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or (
            request.user.is_authenticated and request.user.is_admin()
        )


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    """Доступ только владельцу или чтение."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS) or (
            obj.author == request.user or request.user.is_moderator()
        )


class IsAdmin(permissions.BasePermission):
    """Доступ только администратору."""
    def has_permission(self, request, view):
        return request.user.is_admin()
