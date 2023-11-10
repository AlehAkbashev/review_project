from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class ReaderOrAdmin(permissions.BasePermission):
    """
    Права доступа для чтения или администратора.
    Разрешает доступ только для чтения (GET) или для администратора.
    Methods:
    - has_permission: Проверяет разрешение доступа на уровне представления.
    - has_object_permission: Проверяет разрешение доступа на уровне объекта.
    """

    def has_permission(self, request, view):
        """
        Проверяет разрешение доступа на уровне представления.
        Parameters:
        - request: Запрос пользователя.
        - view: Представление, к которому выполняется запрос.
        Returns:
        - bool: True, если доступ разрешен, иначе False.
        """
        if request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated
                and request.user.is_admin
        ):
            return True


class AdminAccess(permissions.BasePermission):
    """
    Права доступа для администратора.

    Разрешает доступ только для администратора.

    Methods:
    - has_permission: Проверяет разрешение доступа на уровне представления.
    """

    def has_permission(self, request, view):
        """
        Проверяет разрешение доступа на уровне представления.

        Parameters:
        - request: Запрос пользователя.
        - view: Представление, к которому выполняется запрос.

        Returns:
        - bool: True, если доступ разрешен, иначе False.
        """
        return request.user.is_admin or request.user.is_superuser


class CommentReviewPermission(permissions.BasePermission):
    """
    Права доступа для комментариев к обзорам.

    Разрешает доступ только для аутентифицированных пользователей.
    Для объектов разрешает доступ только для чтения (GET) или
    для автора комментария, администратора,
    модератора или суперпользователя.

    Methods:
    - has_permission: Проверяет разрешение доступа на уровне представления.
    - has_object_permission: Проверяет разрешение доступа на уровне объекта.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет разрешение доступа на уровне объекта.

        Parameters:
        - request: Запрос пользователя.
        - view: Представление, к которому выполняется запрос.
        - obj: Объект, к которому выполняется запрос.

        Returns:
        - bool: True, если доступ разрешен, иначе False.
        """
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user == obj.author
                or request.user.is_admin
                or request.user.is_moderator
            )
        )
