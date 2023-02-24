from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Title(models.Model):
    pass


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews", blank=True, null=True
    )
    score = models.IntegerField(validators=(MinValueValidator(1),
                                            MaxValueValidator(10)))

    def __str__(self):
        return self.text

    class Meta:
        constraints = [UniqueConstraint(fields=['author', 'title'],
                       name='unique_rating')]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
