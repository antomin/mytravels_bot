# Generated by Django 4.2.2 on 2023-07-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv_app', '0003_adv_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advphoto',
            name='url',
            field=models.FileField(upload_to='adv_images', verbose_name='изображение'),
        ),
    ]