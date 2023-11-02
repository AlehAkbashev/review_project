from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class ReaderOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin' or request.user.is_superuser


class AdminAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class CommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return not request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user == obj.author
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser
            )