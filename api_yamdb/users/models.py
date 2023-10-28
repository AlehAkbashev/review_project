from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_username


class User(AbstractUser):
    CHOICES = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin")
    )

    email = models.EmailField(unique=True, max_length=254)
    username = models.SlugField(
        unique=True,
        max_length=150,
        validators=[validate_username]
    )
    password = models.CharField(blank=True, null=True, max_length=255)
    bio = models.TextField(blank=True, verbose_name="Biography")
    role = models.SlugField(
        default='user',
        verbose_name='Role',
        choices=CHOICES
    )
    confirmation_code = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return str(self.username)
