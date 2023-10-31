from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class ReaderOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        else:
            if (request.user.is_authenticated
                    and request.user.role == 'admin') or request.user.is_superuser:
                return True
            return False
        return (
            request.user.is_authenticated
            and (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        )


    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or request.user.is_superuser


class AdminAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser
