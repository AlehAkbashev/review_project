from django.contrib.auth import get_user_model
from django.db import models

from api_yamdb.settings import (
    REVIEW_TEXT_MAX_LENGTH,
    TITLE_NAME_MAX_LENGTH
)

from .mixins import CommonDataAbstractModel
from .validators import validate_year

User = get_user_model()


class Category(CommonDataAbstractModel):
    """
    Модель для категорий.
    """

    class Meta(CommonDataAbstractModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

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
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name
    
    @property
    def slug_name(self):
        return {"name": self.name, "slug": self.slug}


class Title(models.Model):
    """
    Модель для заголовков.
    """

    name = models.CharField(
        max_length=TITLE_NAME_MAX_LENGTH,
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
        related_name="categories",
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="title_genres",
        related_name="genre",
        through="TitleGenre",
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовки'

    def __str__(self):
        return self.name


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


class Review(models.Model):
    """
    Модель для отзывов.
    """

    text = models.TextField(
        max_length=REVIEW_TEXT_MAX_LENGTH,
        verbose_name="review_text"
    )
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
        choices=[
            (i, i) for i in range(1, 11)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="review_pub_date"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_author_title"
            )
        ]
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель для комментариев.
    """

    text = models.TextField(
        verbose_name="comment_text"
    )
    review = models.ForeignKey(
        "Review",
        on_delete=models.CASCADE,
        verbose_name="comment_review",
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="comment_author",
        related_name="comments",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="comment_pub_date"
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
