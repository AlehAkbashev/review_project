from django.conf import settings as s
from django.db import models


class CommonDataAbstractModel(models.Model):
    """
    Абстрактная модель для хранения одинаковых
    полей моделей Category и Genre.
    """

    name = models.CharField(
        max_length=s.COMMON_MAX_LENGTH, verbose_name="category_name"
    )
    slug = models.SlugField(
        verbose_name="category_slug",
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('-name',)

    def __str__(self):
        return self.name[:s.NAME_OBJECT_MAX_LENGTH]


class CommonDataAbstractModelTwo(models.Model):
    """
    Абстрактная модель для хранения одинаковых полей
    моделей Comment и Review.
    """

    text = models.TextField(
        max_length=s.COMMON_MAX_LENGTH,
        verbose_name="review_text"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="comment_pub_date"
    )

    class Meta:
        abstract = True
        ordering = ('-name',)

    def __str__(self):
        return self.text[:s.NAME_OBJECT_MAX_LENGTH]
