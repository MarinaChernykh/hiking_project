from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators

from . import constants


User = get_user_model()


class Region(models.Model):
    name = models.CharField(
        'Название региона',
        max_length=50,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
    )
    description = models.TextField(
        'Описание региона',
        blank=True,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='trails/regions',
        blank=True,
    )

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return self.name


class Trail(models.Model):

    LEVEL_CHOICE = (
        ('easy', 'Простой'),
        ('middle', 'Средний'),
        ('hard', 'Сложный')
    )
    TRAIL_TYPE_CHOICE = (
        ('loop', 'Круговой'),
        ('point', 'Туда-обратно'),
    )

    name = models.CharField(
        'Название трека',
        max_length=200,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
    )
    short_description = models.TextField(
        'Короткое описание маршрута',
        blank=True,
    )
    full_description = models.TextField(
        'Полное описание маршрута',
        blank=True,
    )
    start_point_description = models.TextField(
        'Описание дороги до начала маршрута',
        blank=True,
    )
    start_point = models.CharField(
        'Координаты начала маршрута',
        max_length=25,
        validators=[
            validators.RegexValidator(
                regex=constants.COORDINATES)],
        blank=True,
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        related_name='trails',
        blank=True,
        null=True,
        verbose_name='Регион',
    )
    level = models.CharField(
        'Сложность маршрута',
        max_length=6,
        choices=LEVEL_CHOICE,
        blank=True,
    )
    distance = models.FloatField(
        'Продолжительность маршрута в км',
        blank=True,
        null=True,
    )
    time = models.TimeField(
        'Продолжительность маршрута по времени',
        blank=True,
        null=True,
    )
    elevation_gain = models.PositiveSmallIntegerField(
        'Набор высоты в метрах',
        blank=True,
        null=True,
    )
    aqua = models.TextField(
        'Вода на маршруте',
        blank=True,
    )
    route_type = models.CharField(
        'Вид маршрута',
        max_length=5,
        choices=TRAIL_TYPE_CHOICE,
        blank=True,
    )
    route_image = models.ImageField(
        'Карта маршрута',
        upload_to='trails/maps',
        blank=True,
    )
    created = models.DateTimeField(
        'Дата создания статьи',
        auto_now_add=True,
        db_index=True,
    )
    is_published = models.BooleanField(
        'Статус публикации',
        default=False
    )


class Photo(models.Model):
    trail = models.ForeignKey(
        Trail,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Маршрут',
    )
    image = models.ImageField(
        'Фото маршрута',
        upload_to='trails/photos',
        blank=True,
    )


class Comment(models.Model):
    RANK_CHOICE = (
        (1, '1 - Совсем не понравился'),
        (2, '2 - Скорее не понравился'),
        (3, '3 - Понравился, но не сильно'),
        (4, '4 - Понравился'),
        (5, '5 - Очень понравился'),
    )

    trail = models.ForeignKey(
        Trail,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Маршрут',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Комментарий',
        blank=True,
    )
    ranking = models.SmallIntegerField(
        'Оценка',
        choices=RANK_CHOICE,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
