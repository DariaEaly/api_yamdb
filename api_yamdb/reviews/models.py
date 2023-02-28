from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


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

