from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core import validators
from django.urls import reverse


User = get_user_model()


class BaseModel(models.Model):
    """
    Abstact model to add creation and update datetime.
    """
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        'Дата изменения',
        auto_now=True
    )

    class Meta:
        abstract = True


class Region(BaseModel):
    """Information about regions."""
    name = models.CharField(
        'Название региона',
        max_length=50,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
    )
    description_intro = models.TextField(
        'Общая информация',
        blank=True,
    )
    description_seasons = models.TextField(
        'Когда лучше ехать',
        blank=True,
    )
    description_geo = models.TextField(
        'География региона',
        blank=True,
    )
    description_transport = models.TextField(
        'Как добраться',
        blank=True,
    )
    description_accommodation = models.TextField(
        'Где остановиться',
        blank=True,
    )
    main_image = models.ImageField(
        'Главный баннер',
        upload_to='regions/main/',
    )
    mobile_image = models.ImageField(
        'Главный баннер для мобильных',
        upload_to='regions/main/',
    )

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ('id',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'trails:region_detail',
            kwargs={'slug_region': self.slug}
        )


class Trail(BaseModel):
    """Information about trails."""

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
        max_length=100,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=100,
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
                regex=settings.COORDINATES_FORMAT)],
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
        'Сложность',
        max_length=6,
        choices=LEVEL_CHOICE,
        blank=True,
    )
    distance = models.PositiveSmallIntegerField(
        'Длина, км',
        blank=True,
        null=True,
    )
    time = models.CharField(
        'Время',
        max_length=50,
        blank=True,
    )
    elevation_gain = models.PositiveSmallIntegerField(
        'Набор высоты, м',
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
    route_image = models.URLField(
        'Карта маршрута',
        blank=True,
    )
    main_image = models.ImageField(
        'Главный баннер',
        upload_to='trails/main',
    )
    mobile_image = models.ImageField(
        'Главный баннер для мобильных',
        upload_to='trails/main',
    )
    card_image = models.ImageField(
        'Фото для карточки маршрута',
        upload_to='trails/cards',
    )
    previous_trail = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous',
        verbose_name='Предыдущий маршрут'
    )
    next_trail = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next',
        verbose_name='Следующий маршрут'
    )
    is_published = models.BooleanField(
        'Статус публикации',
        default=False
    )

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'trails:trail_detail',
            kwargs={'slug_trail': self.slug}
        )


class RegionPhoto(models.Model):
    """Contains regions images."""
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Регион',
    )
    image = models.ImageField(
        'Фото региона',
        upload_to='regions/photos',
        blank=True,
    )

    class Meta:
        verbose_name = 'Фото региона'
        verbose_name_plural = 'Фото региона'


class TrailPhoto(models.Model):
    """Contains trails images."""
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

    class Meta:
        verbose_name = 'Фото маршрута'
        verbose_name_plural = 'Фото маршрута'


class Comment(BaseModel):
    """Contains users ratings and comments to trails."""
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
    is_active = models.BooleanField(
        'Статус публикации',
        default=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['-created'])
        ]
        constraints = [
            models.CheckConstraint(
                check=(~Q(text__exact='')) | Q(ranking__isnull=False),
                name='not_both_empty',
                violation_error_message='Вы должны заполнить хотя бы одно поле'
            )
        ]

    def __str__(self):
        return f'Автор: {self.author.username}, дата: {self.created}'


class Favorite(models.Model):
    """Contains users favorite trails."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_trails',
        verbose_name='Пользователь'
    )
    trail = models.ForeignKey(
        Trail,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Хочет пройти'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'trail'),
                name='unique_favorite',
            ),
        )
