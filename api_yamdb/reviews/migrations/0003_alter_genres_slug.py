# Generated by Django 3.2 on 2023-10-29 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_genretitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genres',
            name='slug',
            field=models.CharField(max_length=50, unique=True, verbose_name='genres_slug'),
        ),
    ]
