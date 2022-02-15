from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    ROLE_CHOICES = (
        ('USER', 'Пользователь'),
        ('MODERATOR', 'Модератор'),
        ('ADMIN', 'Администратор'),
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', choices=ROLE_CHOICES,
                            default='USER', max_length=5)
    email = models.EmailField('E-MAIL', unique=True, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
