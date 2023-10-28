from rest_framework.permissions import BasePermission


class AdminAccess(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser
    

# class UserMeAccess(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user == self