from rest_framework import permissions


class ReaderOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if (request.user.is_authenticated
                    and request.user.role == 'admin'):
                return True
            return False

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'


class AdminAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser
