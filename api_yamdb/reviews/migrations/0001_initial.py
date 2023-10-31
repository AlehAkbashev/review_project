# Generated by Django 3.2 on 2023-10-31 10:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='category_name')),
                ('slug', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message="Slug doesn't correct", regex='^[-a-zA-Z0-9_]+$')], verbose_name='category_slug')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='comment_text')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='comment_pub_date')),
                ('slug', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message="Slug doesn't correct", regex='^[-a-zA-Z0-9_]+$')], verbose_name='category_slug')),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='genres_name')),
                ('slug', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')], verbose_name='genres_slug')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='review_text')),
                ('score', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], verbose_name='review_score')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='review_pub_date')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='title_name')),
                ('year', models.IntegerField(verbose_name='title_year')),
                ('description', models.TextField(blank=True, verbose_name='title_description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='reviews.categories', verbose_name='title_categories')),
                ('genre', models.ManyToManyField(related_name='genres', through='reviews.GenreTitle', to='reviews.Genres', verbose_name='title_genres')),
            ],
        ),
        migrations.CreateModel(
            name='TitleGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Genresgenres', to='reviews.genres', verbose_name='genreTitle_genres')),
                ('title_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Titlestitles', to='reviews.title', verbose_name='genreTitle_titles')),
            ],
        ),
    ]
