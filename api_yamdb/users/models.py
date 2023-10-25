from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICES = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin")
    )

    email = models.EmailField(unique=True, max_length=254)
    username = models.SlugField(unique=True, max_length=150)
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

    def __str__(self) -> str:
        return self.username
