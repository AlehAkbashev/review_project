from django.conf import settings as s
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    """
    Пользователь.
    Расширение модели AbstractUser с добавлением дополнительных полей.
    """

    CHOICES = (
        (s.USER_ROLE, "user"),
        (s.MODERATOR_ROLE, "moderator"),
        (s.ADMIN_ROLE, "admin"),
    )

    email = models.EmailField(
        unique=True,
        max_length=s.EMAIL_MAX_LENGTH
    )
    username = models.CharField(
        unique=True,
        max_length=s.USERNAME_MAX_LENGTH,
        validators=[validate_username,
                    RegexValidator(regex=r"^[\w.@+-]+\Z")],
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография")
    role = models.SlugField(
        max_length=s.ROLE_MAX_LENGTH,
        default=s.USER_ROLE,
        verbose_name="Role",
        choices=CHOICES,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        """
        Проверяет, является ли пользователь администратором.
        Возвращает True, если роль пользователя равна "admin"
        или если пользователь является
        суперпользователем или стаффом, иначе False.
        """
        return self.role == s.ADMIN_ROLE or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        """
        Проверяет, является ли пользователь модератором.
        Возвращает True, если роль пользователя равна "moderator", иначе False.
        """
        return self.role == s.MODERATOR_ROLE

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта User (имя пользователя).
        """

        return str(self.username)
