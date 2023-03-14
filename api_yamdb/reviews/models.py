from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название произведения',
        max_length=100,
    )
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор',
        help_text='Введите уникальный идентификатор группы',
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        help_text='Введите название жанра',
        max_length=100,
    )
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор',
        help_text='Введите уникальный идентификатор',
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=50,
        db_index=True,
        help_text='Введите название',
        verbose_name='Название произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
        help_text='Выберите категорию',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='Жанр',
        help_text='Выберите жанр',
    )
    year = models.IntegerField(
        verbose_name='Год публикации',
        help_text='Введите год публикации произведения',
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        null=True,
        help_text='Введите описание произведения',
        blank=True,
    )

    class Meta:
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовки'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return (
            f'Жанр - {self.genre} произведения - {self.title}'
        )


class Review(models.Model):
    """Отзывы"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=10,
                message='Введите целое число от 1 до 10'
            ),
            MinValueValidator(
                limit_value=1,
                message='Введите целое число от 1 до 10'
            )
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    """Комментарии к отзывам"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
