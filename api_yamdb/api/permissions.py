from rest_framework import permissions
from rest_framework.permissions import BasePermission

class ReaderOrAdmin(BasePermission):
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
    

class AdminAccess(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
    

class UserMeAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == self