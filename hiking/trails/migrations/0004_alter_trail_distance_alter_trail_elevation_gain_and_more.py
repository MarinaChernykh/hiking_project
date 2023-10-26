# Generated by Django 4.2.6 on 2023-10-24 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trails', '0003_alter_regionphoto_options_alter_trailphoto_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trail',
            name='distance',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Длина, км'),
        ),
        migrations.AlterField(
            model_name='trail',
            name='elevation_gain',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Набор высоты, м'),
        ),
        migrations.AlterField(
            model_name='trail',
            name='level',
            field=models.CharField(blank=True, choices=[('easy', 'Простой'), ('middle', 'Средний'), ('hard', 'Сложный')], max_length=6, verbose_name='Сложность'),
        ),
        migrations.AlterField(
            model_name='trail',
            name='time',
            field=models.CharField(blank=True, max_length=50, verbose_name='Время'),
        ),
    ]
