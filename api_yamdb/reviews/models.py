import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    # Выбор начальных категорий
    CATEGORY_CHOICES = (
        ('MUSIC', 'Музыка'),
        ('FILM', 'Фильмы'),
        ('BOOK', 'Книги'),
    )
    name = models.CharField(max_length=200,
                            null=False,
                            verbose_name='название категории')
    slug = models.SlugField(
        unique=True,
        verbose_name="url-адрес категории",
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50,
                            null=False,
                            verbose_name='название жанра')
    slug = models.SlugField(
        unique=True,
        verbose_name="url-адрес жанра",
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.datetime.now().year)
        ],
        verbose_name="Год выпуска",
    )
    description = models.TextField(max_length=500, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        blank=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", null=True,
    )
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведения')
    text = models.TextField(max_length=200, verbose_name='Текст отзыва')
    score = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)],
        error_messages={'validators': 'Укажите оценку от 1 до 10'},
        verbose_name='Оценка')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        null=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        # Данная команда не даст повторно голосовать
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='Отзыв', null=True
    )
    text = models.TextField('Текст комментария', max_length=200)
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, null=True
    )

    # class Meta:
    #     ordering = ['-created']

    def __str__(self):
        return self.text
