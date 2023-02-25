from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.TextField()
    bio = models.TextField()


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('URL категории', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('URL жанра', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=200)
    year = models.IntegerField('Год выпуска')
    description = models.TextField(
        'Описание произведения', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр',
        through='TitleGenre')
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles')
    rating = models.IntegerField('Рейтинг', blank=True, null=True)

    def __str__(self):
        return self.title


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
