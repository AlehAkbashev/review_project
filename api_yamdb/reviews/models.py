from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=256, verbose_name='category_name')
    slug = models.CharField(max_length=50, verbose_name='category_slug')

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256, verbose_name='genres_name')
    slug = models.CharField(max_length=50, verbose_name='genres_slug')

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='title_name')
    year = models.IntegerField(verbose_name='title_year')
    description = models.TextField(blank=True, verbose_name='title_description')
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        verbose_name='title_categories',
        related_name='categories')
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='title_genres',
        related_name='genres')

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(
        'text',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
    )


class Review(models.Model):
    name = models.CharField(
        'Имя',
        max_length=256,
    )
    text = models.CharField(
        Comment,
        max_length=256,

    )
    rating = models.IntegerField(

    )
