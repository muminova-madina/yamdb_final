from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

from reviews.validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель категорий произвудений."""

    name = models.TextField(
        verbose_name='Категория',
        max_length=settings.NAME_FIELD_MAX_LENGTH,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Ссылка',
        max_length=settings.SLUG_FIELD_MAX_LENGTH,
    )

    class Meta:
        verbose_name = ('Категория произведения',)
        verbose_name_plural = 'Категории произведения'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанров."""
    name = models.TextField(
        verbose_name='Жанр',
        max_length=settings.NAME_FIELD_MAX_LENGTH,
    )
    slug = models.SlugField(
        unique=True,
        max_length=settings.SLUG_FIELD_MAX_LENGTH,
        verbose_name='Ссылка',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель для произведений."""

    name = models.TextField(
        verbose_name='Произведение',
        max_length=settings.NAME_FIELD_MAX_LENGTH,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год опубликования',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория произведения',
        null=True,
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='titles',
        verbose_name='Жанры произведения',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:32]


class Review(models.Model):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв на произведение',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва',
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        verbose_name='Оценка произведения',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'), name='one_review_per_title'
            ),
        )

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    """Модель комментарий."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв на произведение',
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментатор',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.author}_{self.text[:10]}'


class TitleGenre(models.Model):
    """ Базовая модель жанров и произведений."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
