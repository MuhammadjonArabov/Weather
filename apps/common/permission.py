from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsRegisteredAndLoggedIn(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied({"message": 'User not authenticated 👎'})
        return True
