from django.contrib.auth import get_user_model
from django.conf import settings as s
from django.db import models

User = get_user_model()


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
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="review_author",
        related_name="reviews",
    )

    class Meta:
        abstract = True
        ordering = ('-name',)

    def __str__(self):
        return self.text[:s.NAME_OBJECT_MAX_LENGTH]
