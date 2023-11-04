import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

User = get_user_model()


def import_data():
    with open("static/data/users.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6],
            )

    with open("static/data/category.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            Category.objects.get_or_create(id=row[0], name=row[1], slug=row[2])

    with open("static/data/genre.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            Genre.objects.get_or_create(id=row[0], name=row[1], slug=row[2])

    with open("static/data/titles.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=Category.objects.get(id=row[3]),
            )

    with open("static/data/review.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            Review.objects.get_or_create(
                id=row[0],
                title_id=row[1],
                text=row[2],
                author=User.objects.get(id=row[3]),
                score=row[4],
                pub_date=row[5],
            )

    with open("static/data/genre_title.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            TitleGenre.objects.get_or_create(
                id=row[0],
                title_id=Title.objects.get(id=row[1]),
                genre_id=Genre.objects.get(id=row[2]),
            )

    with open("static/data/comments.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            Comment.objects.get_or_create(
                id=row[0],
                review_id=row[1],
                text=row[2],
                author=User.objects.get(id=row[3]),
                pub_date=row[4],
            )


class Command(BaseCommand):
    help = "Imports data from a CSV file into the YourModel model"

    def handle(self, *args, **options):
        import_data()
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
