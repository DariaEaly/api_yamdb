from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Модель для представления пользователя."""

    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Username"
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
        verbose_name="Электронная почта"
    )

    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name="Имя"
    )

    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name="Фамилия"
    )

    confirmation_code = models.CharField(
        max_length=99,
        blank=True,
        null=True,
        editable=False,
        unique=True,
        verbose_name="Код подтверждения",
    )
    bio = models.TextField(blank=True, verbose_name="О себе")
    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.USER,
        verbose_name="Роль",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.first_name} ${self.last_name} ({self.username})'

    @property
    def is_admin(self):
        return (self.role == Role.ADMIN
                or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('URL категории', max_length=50, unique=True)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('URL жанра', max_length=50, unique=True)

    class Meta:
        ordering = ('-name',)

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


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews", blank=True, null=True,
        verbose_name='Произведение'
    )
    score = models.IntegerField(validators=(MinValueValidator(1),
                                            MaxValueValidator(10)),
                                verbose_name='Рейтинг произведения')

    def __str__(self):
        return self.text

    class Meta:
        constraints = [UniqueConstraint(fields=['author', 'title'],
                       name='unique_rating')]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв')
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата добавления')
