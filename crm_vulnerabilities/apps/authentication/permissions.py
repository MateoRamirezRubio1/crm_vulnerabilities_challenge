from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Permiso para rol admin"""

    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"


class IsAdvancedUser(BasePermission):
    """Permiso para usuarios avanzados"""

    def has_permission(self, request, view):
        return request.user and request.user.role == "advanced"


class IsBasicUser(BasePermission):
    """Permiso para usuarios básicos"""

    def has_permission(self, request, view):
        return request.user and request.user.role == "basic"
