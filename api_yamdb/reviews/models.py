from django.db import models


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
    genre = models.ManyToManyField(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='title_genres',
        related_name='genres')

    def __str__(self):
        return self.name
