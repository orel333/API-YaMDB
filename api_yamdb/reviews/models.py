import datetime
import logging
import sys

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
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
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                '"is_staff" суперпользователя должно быть в режиме "True"'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                '"is_superuser" суперпользователя должно быть в режиме "True"'
            )
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


class Category(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='название категории')
    slug = models.SlugField(
        unique=True,
        verbose_name="url-адрес категории",
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='название жанра')
    slug = models.SlugField(
        unique=True,
        verbose_name="url-адрес жанра",
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name="Название произведения")
    year = models.PositiveIntegerField(
        verbose_name="Год создания",
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.datetime.now().year)
        ],
    )
    description = models.TextField(max_length=500, blank=True,
                                   verbose_name="описание")
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        blank=True, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", null=True,
        blank=True, verbose_name='Категория'
    )

    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',verbose_name='Произведения', null=True)
    text = models.TextField(max_length=200, verbose_name='Текст отзыва')
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)],
        error_messages={'validators': 'Укажите оценку от 1 до 10'},
        verbose_name='Оценка',
        )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        null=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # Данная команда не даст повторно голосовать
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_review'
            )]
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, null=True,
        related_name="comments", verbose_name='Произведение'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments', verbose_name='Отзыв', null=True
    )
    text = models.TextField('Текст комментария', max_length=200)
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, null=True
    )
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


