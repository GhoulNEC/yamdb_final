from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year


class GenreCategoryBase(models.Model):
    """Абстрактная модель для жанров и категорий"""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('slug', max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Genre(GenreCategoryBase):
    """Модель жанры, многое к многому"""
    pass


class Category(GenreCategoryBase):
    """Модель категории одно к многим """

    class Meta(GenreCategoryBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель Произведение, базовая модель"""

    name = models.TextField('Название произведения')
    year = models.PositiveSmallIntegerField(
        'Год релиза',
        validators=[validate_year],
        help_text='Введите год релиза'
    )
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Введите категорию произведения',
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self) -> str:
        return self.name


class ReviewCommentBase(models.Model):
    """Абстрактная модель для отзывов и комментариев"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField('Текст')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Review(ReviewCommentBase):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        default=1,
        validators=[
            MaxValueValidator(10, message='Оценка не может быть выше "10"'),
            MinValueValidator(1, message='Оценка не может быть ниже "1"')
        ],
    )

    class Meta(ReviewCommentBase.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review")
        ]
        default_related_name = 'reviews'


class Comment(ReviewCommentBase):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
