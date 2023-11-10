from django.conf import settings as s
from django.contrib.auth import get_user_model
from django.db import models

from reviews.abstract_models import (CommonDataAbstractModel,
                                     CommonDataAbstractModelTwo)
from reviews.validators import validate_year

User = get_user_model()


class Category(CommonDataAbstractModel):
    """
    Модель для категорий.
    """

    class Meta(CommonDataAbstractModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    @property
    def slug_name(self):
        return {"name": self.name, "slug": self.slug}


class Genre(CommonDataAbstractModel):
    """
    Модель для жанров.
    """

    class Meta(CommonDataAbstractModel.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name[:s.OBJECT_MAX_LENGTH]


class Title(models.Model):
    """
    Модель для заголовков.
    """

    name = models.CharField(
        max_length=s.COMMON_MAX_LENGTH,
        verbose_name="title_name"
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="title_year",
        validators=[
            validate_year,
        ],
    )
    description = models.TextField(
        blank=True,
        verbose_name="title_description"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="title_categories",
        related_name="titles",
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="title_genres",
        related_name="titles",
        through="TitleGenre",
    )

    class Meta:
        ordering = ["-name"]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name[:s.OBJECT_MAX_LENGTH]


class TitleGenre(models.Model):
    """
    Модель для связи заголовков и жанров.
    """

    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="title_titles",
        related_name="titles_titles",
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="title_genres",
        related_name="genre_genres",
    )

    def __str__(self):
        return f"{self.title_id} {self.genre_id}"


class Review(CommonDataAbstractModelTwo):
    """
    Модель для отзывов.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="review_title",
        related_name="reviews",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="review_author",
        related_name="reviews",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="review_score",
        choices=[(i, i) for i in range(1, 11)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_author_title"
            )
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(CommonDataAbstractModelTwo):
    """
    Модель для комментариев.
    """

    review = models.ForeignKey(
        "Review",
        on_delete=models.CASCADE,
        verbose_name="comment_review",
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="comment_author",
        related_name="comments",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
