# Generated by Django 4.2.6 on 2023-11-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='mobile_image',
            field=models.ImageField(blank=True, upload_to='regions/main/', verbose_name='Главный баннер для мобильных'),
        ),
        migrations.AddField(
            model_name='trail',
            name='mobile_image',
            field=models.ImageField(blank=True, upload_to='trails/main', verbose_name='Главный баннер для мобильных'),
        ),
    ]