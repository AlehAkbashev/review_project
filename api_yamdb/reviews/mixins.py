from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import (
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH
)


class CommonDataAbstractModel(models.Model):
    """
    Абстрактная модель для хранения одинаковых
    полей моделей Category и Genre.
    """

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="category_name"
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Slug is not correct'
            )
        ],
        verbose_name="category_slug",
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ['-name']
