import logging
import sys

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models

from api.methods import encode, give_jwt_for

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s - строка %(lineno)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
handler.setFormatter(formatter)
logger.disabled = False
logger.debug('Логирование из models запущено')



ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)

class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        #other_fields.setdefault('role', 'admin')
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                '"is_staff" суперпользователя должно быть в режиме "True"'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                '"is_superuser" суперпользователя должно быть в режиме "True"'
            )

        # user = super().create_superuser(username, email, password)
        # user.role = 'admin'
        # user.save(using=self._db)
        # выдаем суперпользователю confirmation_code
        # dict = {
            # 'email': email,
            # 'username': username
        # }
        # confirmation_code = encode(dict)
        # token = give_jwt_for(user, is_superuser=True)
        # print(f'\n\tДобро пожаловать, суперпользователь {username}!\n\n'
              # f'Ваш токен: \n\n{token}\n\n'
              # f'Ваш confirmation_code:\n\n{confirmation_code}\n'
              # f'- используйте его при необходимости обновления токена.')
# 
        # выдаем суперпользователю token
        role = 'admin'

        return self.create_user(username, email, role, password, **other_fields)

    def create_user(self, username, email, role='user', password=None, **other_fields):
        logger.debug(f'Got role: {role}')
        logger.debug(f'Got password: {password}')
        logger.debug('Create user func was initiated')
        if not email:
            raise ValueError('Необходимо указать email')
        if not username:
            raise ValueError('Необходимо указать username')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            role=role,
            **other_fields
        )
        if role == 'admin':
            user.is_staff = True
            user.set_password(password)
        user.save()
        dict = {
            'email': email,
            'username': username
        }
        confirmation_code = encode(dict)
        if user.is_superuser == True:
            token = give_jwt_for(user, is_superuser=True)
            first_line = f'Создан суперпользователь {username}.\n'
        else:
            first_line = f'Создан пользователь {username}.\n'
            token = give_jwt_for(user)


        print(f'{first_line}Его роль: {role}.'
              f'Его токен: {token}\n'
              f'Его confirmation_code для обновления токена:\n'
              f'{confirmation_code}')
        return user


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
    #is_superuser = models.BooleanField(default=False)
    #is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

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