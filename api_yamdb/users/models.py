from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        choices=ROLE_CHOICES,
        default='user',
        max_length=16
    )
    email = models.EmailField('E-MAIL', unique=True, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.username}: {self.email}, уровень доступа: {self.role}'


class PreUser(models.Model):
    email = models.EmailField('E-MAIL', unique=True, blank=False, null=False)
    username = models.CharField('username', max_length=150, unique=True)

    class Meta:
        verbose_name = 'предпользователь'
        verbose_name_plural = 'предпользователи'

    def __str__(self):
        return f'{self.username}: {self.email}'
