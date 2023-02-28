from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Title(models.Model):
    pass


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
