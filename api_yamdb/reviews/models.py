from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import datetime

class Category(models.Model):
    #Выбор начальных категорий
    CATEGORY_CHOICES = (
        ('MUSIC', 'Музыка'),
        ('FILM', 'Фильмы'),
        ('BOOK', 'Книги'),
    )
    name = models.CharField(max_length=200,
                            choices=CATEGORY_CHOICES,
                            null=False)
    slug = models.SlugField(
        unique=True,
        verbose_name="url-адрес категории",
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, null=False)
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
    description = models.TextField
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name="titles", null=True,
        required=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", null=True,
        required=True,
    )

    def __str__(self):
        return self.name
