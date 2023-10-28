import csv
from django.core.management.base import BaseCommand
from reviews.models import Categories, Genres, Title, Comment, Review,GenreTitle, User

def import_data():

    with open('static/data/users.csv') as csvfile:
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
                last_name=row[6]
            )


    with open('static/data/category.csv') as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            Categories.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )

    with open('static/data/genre.csv') as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        reader.pop(0)
        for row in reader:
            Genres.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )

    # <-----------------------Impotrs Doesnt Work From Here--------------------->

    # with open('static/data/review.csv') as csvfile:
    #     reader = csv.reader(csvfile)
    #     reader = list(reader)
    #     reader.pop(0)
    #     for row in reader:
    #         Review.objects.get_or_create(
    #             id=row[0],
    #             title_id=row[1],
    #             text=row[2],
    #             author=row[3],
    #             score=row[4],
    #             pub_date=row[5]
    #         )

    # with open('static/data/genre_title.csv') as csvfile:
    #     reader = csv.reader(csvfile)
    #     reader = list(reader)
    #     reader.pop(0)
    #     for row in reader:
    #         GenreTitle.objects.get_or_create(
    #             id=row[0],
    #             title_id=row[1],
    #             genre_id=row[2]
    #         )

    # with open('static/data/titles.csv') as csvfile:
    #     reader = csv.reader(csvfile)
    #     reader = list(reader)
    #     reader.pop(0)
    #     for row in reader:
    #         Title.objects.get_or_create(
    #             id=row[0],
    #             name=row[1],
    #             year=row[2],
    #             category=row[3]
    #         )
    #
    # with open('static/data/comments.csv') as csvfile:
    #     reader = csv.reader(csvfile)
    #     reader = list(reader)
    #     reader.pop(0)
    #     for row in reader:
    #         Comment.objects.get_or_create(
    #             id=row[0],
    #             review_id=row[1],
    #             text=row[2],
    #             author=row[3],
    #             pub_date=row[4]
    #
    #         )


class Command(BaseCommand):
    help = 'Imports data from a CSV file into the YourModel model'

    def handle(self, *args, **options):
        import_data()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
