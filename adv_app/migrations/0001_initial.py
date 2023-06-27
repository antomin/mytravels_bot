# Generated by Django 4.2.2 on 2023-06-22 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdvButton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='текст кнопки')),
                ('url', models.URLField(verbose_name='ссылка')),
            ],
            options={
                'verbose_name': 'кнопка',
                'verbose_name_plural': 'кнопки',
            },
        ),
        migrations.CreateModel(
            name='AdvPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название')),
                ('url', models.ImageField(upload_to='adv_images', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'рекламное изображение',
                'verbose_name_plural': 'рекламные изображения',
            },
        ),
        migrations.CreateModel(
            name='Adv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='название кампании')),
                ('text', models.TextField(verbose_name='текст')),
                ('time_exec', models.DateTimeField(verbose_name='время запуска')),
                ('enabled', models.BooleanField(default=False, verbose_name='включена')),
                ('buttons', models.ManyToManyField(blank=True, to='adv_app.advbutton', verbose_name='кнопки')),
                ('photos', models.ManyToManyField(blank=True, to='adv_app.advphoto', verbose_name='вложенные изображения')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
    ]