import csv

from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)


class Command(BaseCommand):
    help = 'Импортирует данные из csv файлов'

    def handle(self, *args, **options):
        paths = {Category: 'static/data/category.csv',
                 Genre: 'static/data/genre.csv'}
        for model, path in paths.items():
            """Запись категорий и жанров."""
            with open(path, encoding="utf-8") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    id = row['id']
                    name = row['name']
                    slug = row['slug']
                    model(id=id, name=name, slug=slug).save()

        with open('static/data/titles.csv', encoding="utf-8") as csv_file:
            """Запись произведений."""
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                year = row['year']
                category = row['category']
                Title(id=id, name=name, year=year, category_id=category).save()

        with open('static/data/genre_title.csv', encoding="utf-8") as csv_file:
            """Добавление жанров к произведениям."""
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                title_id = row['title_id']
                genre_id = row['genre_id']
                TitleGenre(title_id=title_id, genre_id=genre_id).save()

        with open('static/data/review.csv', encoding="utf-8") as csv_file:
            """Запись отзывов."""
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                title_id = row['title_id']
                text = row['text']
                author = row['author']
                score = row['score']
                pub_date = row['pub_date']
                Review(id=id,
                       title_id=title_id,
                       text=text,
                       author=author,
                       score=score,
                       pub_date=pub_date).save()

        with open('static/data/users.csv', encoding="utf-8") as csv_file:
            """Запись пользователей."""
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = row['first_name']
                last_name = row['last_name']
                User(id=id,
                     username=username,
                     email=email,
                     role=role,
                     bio=bio,
                     first_name=first_name,
                     last_name=last_name).save()

        with open('static/data/comments.csv', encoding="utf-8") as csv_file:
            """Запись комментариев."""
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                review_id = row['review_id']
                text = row['text']
                author = row['author']
                pub_date = row['pub_date']
                Comment(id=id,
                        review_id=review_id,
                        text=text,
                        author=author,
                        score=score,
                        pub_date=pub_date).save()
