from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_username
from api_yamdb.settings import (
    ADMIN_ROLE,
    EMAIL_MAX_LENGTH,
    MODERATOR_ROLE,
    PASSWORD_MAX_LENGTH,
    ROLE_MAX_LENGTH,
    USER_ROLE,
    USERNAME_MAX_LENGTH,
)


class User(AbstractUser):
    """
    Пользователь.
    Расширение модели AbstractUser с добавлением дополнительных полей.
    """

    CHOICES = (
        (USER_ROLE, "user"),
        (MODERATOR_ROLE, "moderator"),
        (ADMIN_ROLE, "admin"),
    )

    email = models.EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH
    )
    username = models.CharField(
        unique=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username, RegexValidator(regex=r"^[\w.@+-]+\Z")],
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Biography"
    )
    role = models.SlugField(
        max_length=ROLE_MAX_LENGTH,
        default=USER_ROLE,
        verbose_name="Role",
        choices=CHOICES
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def is_admin(self):
        """
        Проверяет, является ли пользователь администратором.
        Возвращает True, если роль пользователя равна "admin"
        или если пользователь является суперпользователем, иначе False.
        """
        if self.role == "admin" or self.is_superuser:
            return True
        return False

    @property
    def is_moderator(self):
        """
        Проверяет, является ли пользователь модератором.
        Возвращает True, если роль пользователя равна "moderator", иначе False.
        """
        if self.role == "moderator":
            return True
        return False

    @property
    def is_user(self):
        """
        Проверяет, является ли пользователь обычным пользователем.
        Возвращает True, если роль пользователя равна "user", иначе False.
        """
        if self.role == "user":
            return True
        return False

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта User (имя пользователя).
        """
        return str(self.username)
