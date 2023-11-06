from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """
    Пользователь.
    Расширение модели AbstractUser с добавлением дополнительных полей.
    """

    CHOICES = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    )

    email = models.EmailField(unique=True, max_length=254)
    username = models.SlugField(
        unique=True,
        max_length=150,
        validators=[validate_username],
    )
    password = models.CharField(blank=True, null=True, max_length=255)
    bio = models.TextField(blank=True, verbose_name="Biography")
    role = models.SlugField(
        default="user", verbose_name="Role", choices=CHOICES
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
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        """
        Проверяет, является ли пользователь модератором.
        Возвращает True, если роль пользователя равна "moderator", иначе False.
        """
        return self.role == "moderator"

    @property
    def is_user(self):
        """
        Проверяет, является ли пользователь обычным пользователем.
        Возвращает True, если роль пользователя равна "user", иначе False.
        """
        return self.role == "user"

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта User (имя пользователя).
        """
        return str(self.username)
