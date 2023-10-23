# Generated by Django 4.2.6 on 2023-10-23 19:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название региона')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
                ('description_intro', models.TextField(blank=True, verbose_name='Общая информация')),
                ('description_seasons', models.TextField(blank=True, verbose_name='Когда лучше ехать')),
                ('description_geo', models.TextField(blank=True, verbose_name='География региона')),
                ('description_transport', models.TextField(blank=True, verbose_name='Как добраться')),
                ('description_accommodation', models.TextField(blank=True, verbose_name='Где остановиться')),
                ('main_image', models.ImageField(blank=True, upload_to='regions/main/', verbose_name='Главный баннер')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='Trail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название трека')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Слаг')),
                ('short_description', models.TextField(blank=True, verbose_name='Короткое описание маршрута')),
                ('full_description', models.TextField(blank=True, verbose_name='Полное описание маршрута')),
                ('start_point_description', models.TextField(blank=True, verbose_name='Описание дороги до начала маршрута')),
                ('start_point', models.CharField(blank=True, max_length=25, validators=[django.core.validators.RegexValidator(regex='^[-+]?([1-8]?\\d(\\.\\d+)?|90(\\.0+)?),\\s*[-+]?(180(\\.0+)?|((1[0-7]\\d)|([1-9]?\\d))(\\.\\d+)?)$')], verbose_name='Координаты начала маршрута')),
                ('level', models.CharField(blank=True, choices=[('easy', 'Простой'), ('middle', 'Средний'), ('hard', 'Сложный')], max_length=6, verbose_name='Сложность маршрута')),
                ('distance', models.FloatField(blank=True, null=True, verbose_name='Длина маршрута в км')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Время на маршрут в часах')),
                ('elevation_gain', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Набор высоты в метрах')),
                ('aqua', models.TextField(blank=True, verbose_name='Вода на маршруте')),
                ('route_type', models.CharField(blank=True, choices=[('loop', 'Круговой'), ('point', 'Туда-обратно')], max_length=5, verbose_name='Вид маршрута')),
                ('route_image', models.ImageField(blank=True, upload_to='trails/maps', verbose_name='Карта маршрута')),
                ('main_image', models.ImageField(blank=True, upload_to='trails/main', verbose_name='Главный баннер')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания статьи')),
                ('is_published', models.BooleanField(default=False, verbose_name='Статус публикации')),
                ('next_trail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='trails.trail', verbose_name='Следующий маршрут')),
                ('previous_trail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='trails.trail', verbose_name='Предыдущий маршрут')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trails', to='trails.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Маршрут',
                'verbose_name_plural': 'Маршруты',
            },
        ),
        migrations.CreateModel(
            name='TrailPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='trails/photos', verbose_name='Фото маршрута')),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='trails.trail', verbose_name='Маршрут')),
            ],
        ),
        migrations.CreateModel(
            name='RegionPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='regions/photos', verbose_name='Фото региона')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='trails.region', verbose_name='Регион')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Комментарий')),
                ('ranking', models.SmallIntegerField(blank=True, choices=[(1, '1 - Совсем не понравился'), (2, '2 - Скорее не понравился'), (3, '3 - Понравился, но не сильно'), (4, '4 - Понравился'), (5, '5 - Очень понравился')], null=True, verbose_name='Оценка')),
                ('created', models.DateTimeField(db_index=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='trails.trail', verbose_name='Маршрут')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-created',),
                'indexes': [models.Index(fields=['-created'], name='trails_comm_created_ed85f9_idx')],
            },
        ),
    ]