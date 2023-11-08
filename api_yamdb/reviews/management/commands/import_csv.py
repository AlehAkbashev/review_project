import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

User = get_user_model()

dictionary = {
    "static/data/users.csv": User,
    "static/data/category.csv": Category,
    "static/data/genre.csv": Genre,
}


def cut_list_line(csvfile):
    reader = csv.reader(csvfile)
    reader = list(reader)
    reader.pop(0)
    return reader


def import_data():
    for key, value in dictionary.items():
        with open(key, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            objs = [value(**row) for row in reader]
            value.objects.bulk_create(objs)

    with open("static/data/titles.csv", encoding="utf8") as csvfile:
        reader = cut_list_line(csvfile)
        objs = [
            Title(
                id=row[0],
                name=row[1],
                year=row[2],
                category=Category.objects.get(id=row[3]),
            )
            for row in reader
        ]
        Title.objects.bulk_create(objs)

    with open("static/data/review.csv", encoding="utf8") as csvfile:
        reader = cut_list_line(csvfile)
        objs = [
            Review(
                id=row[0],
                title_id=row[1],
                text=row[2],
                author=User.objects.get(id=row[3]),
                score=row[4],
                pub_date=row[5],
            )
            for row in reader
        ]
        Review.objects.bulk_create(objs)

    with open("static/data/genre_title.csv", encoding="utf8") as csvfile:
        reader = cut_list_line(csvfile)
        objs = [
            TitleGenre(
                id=row[0],
                title_id=Title.objects.get(id=row[1]),
                genre_id=Genre.objects.get(id=row[2]),
            )
            for row in reader
        ]
        TitleGenre.objects.bulk_create(objs)

    with open("static/data/comments.csv", encoding="utf8") as csvfile:
        reader = cut_list_line(csvfile)
        objs = [
            Comment(
                id=row[0],
                review_id=row[1],
                text=row[2],
                author=User.objects.get(id=row[3]),
                pub_date=row[4],
            )
            for row in reader
        ]
        Comment.objects.bulk_create(objs)


class Command(BaseCommand):
    help = "Imports data from a CSV file into the YourModel model"

    def handle(self, *args, **options):
        import_data()
        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
