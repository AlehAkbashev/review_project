from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='Categories')
    genre = models.ManyToManyField(
        Genres, on_delete=models.CASCADE, related_name='Genres')

    def __str__(self):
        return self.name
