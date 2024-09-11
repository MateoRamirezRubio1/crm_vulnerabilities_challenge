from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Permission class for admin users"""

    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"


class IsAdvancedUser(BasePermission):
    """Permission class for advanced users"""

    def has_permission(self, request, view):
        return request.user and request.user.role == "advanced"


class IsBasicUser(BasePermission):
    """Permission class for basic users"""

    def has_permission(self, request, view):
        return request.user and request.user.role == "basic"
