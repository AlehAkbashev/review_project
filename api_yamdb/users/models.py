from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_username
from django.core.validators import RegexValidator


class User(AbstractUser):
    CHOICES = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin")
    )

    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[
            validate_username,
            RegexValidator(regex=r"^[\w.@+-]+\Z")
        ]
    )
    password = models.CharField(blank=True, null=True, max_length=255)
    bio = models.TextField(blank=True, verbose_name="Biography")
    role = models.SlugField(
        default='user',
        verbose_name='Role',
        choices=CHOICES
    )


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True
        return False

    @property
    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False

    @property
    def is_user(self):
        if self.role == 'user':
            return True
        return False

    def __str__(self) -> str:
        return str(self.username)

    @property
    def is_admin(self):
        if self.role == 'admin':
            return True
        return False

    @property
    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False

