from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    """
    Модель для категорий.
    """

    name = models.CharField(max_length=256, verbose_name="category_name")
    slug = models.SlugField(
        validators=[
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$", message="Slug doesn't correct"
            )
        ],
        max_length=50,
        verbose_name="category_slug",
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель для жанров.
    """

    name = models.CharField(max_length=256, verbose_name="genres_name")
    slug = models.SlugField(
        max_length=50,
        verbose_name="genres_slug",
        unique=True,
        validators=[RegexValidator(regex=r"^[-a-zA-Z0-9_]+$")],
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Модель для заголовков.
    """

    name = models.CharField(max_length=256, verbose_name="title_name")
    year = models.IntegerField(
        verbose_name="title_year",
        validators=[
            validate_year,
        ],
    )
    description = models.TextField(
        blank=True, verbose_name="title_description"
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
        related_name="genres",
        through="TitleGenre",
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """
    Модель для связи заголовков и жанров.
    """

    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="genreTitle_titles",
        related_name="Titlestitles",
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="genreTitle_genres",
        related_name="Genresgenres",
    )

    def __str__(self):
        return f"{self.title_id} {self.genre_id}"


class Comment(models.Model):
    """
    Модель для комментариев.
    """

    text = models.TextField(verbose_name="comment_text")
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
        auto_now_add=True, verbose_name="comment_pub_date"
    )

    def __str__(self):
        return self.text


class Review(models.Model):
    """
    Модель для отзывов.
    """

    text = models.TextField(verbose_name="review_text")
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
    score = models.PositiveIntegerField(
        verbose_name="review_score", choices=[(i, i) for i in range(1, 11)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="review_pub_date"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title"
            )
        ]

    def __str__(self):
        return self.text
