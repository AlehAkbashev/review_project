from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=256, verbose_name='category_name')
    slug = models.CharField(
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$', message="Slug doesn't correct")],
        max_length=50,
        verbose_name='category_slug',
        blank=False,
        unique=True
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256, verbose_name='genres_name')
    slug = models.CharField(
        max_length=50,
        verbose_name='genres_slug',
        unique=True,
        validators=[RegexValidator(regex=r"^[-a-zA-Z0-9_]+$")]
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='title_name')
    year = models.IntegerField(verbose_name='title_year')
    description = models.TextField(
        blank=True,
        verbose_name='title_description'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        verbose_name='title_categories',
        related_name='categories')
    genre = models.ManyToManyField(
        Genres,
        verbose_name='title_genres',
        related_name='genres',
        through='GenreTitle'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='genreTitle_titles',
        related_name='Titlestitles'
    )
    genre_id = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='genreTitle_genres',
        related_name='Genresgenres'
    )

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Comment(models.Model):
    text = models.TextField(verbose_name='comment_text')
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        verbose_name='comment_review',
        related_name='comments')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='comment_author',
        related_name='comments')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='comment_pub_date')

    def __str__(self):
        return self.text


class Review(models.Model):
    text = models.TextField(verbose_name='review_text')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='review_title',
        related_name='reviews')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='review_author',
        related_name='reviews')
    score = models.PositiveIntegerField(
        verbose_name='review_score',
        choices=[(i, i) for i in range(1, 11)])
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='review_pub_date')

    def __str__(self):
        return self.text
