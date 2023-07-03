# Generated by Django 4.2.2 on 2023-07-03 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot_app', '0011_rename_arrival_date_flightsubscription_return_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='end_subscription',
            field=models.DateTimeField(blank=True, null=True, verbose_name='окончание подписки'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_subscriber',
            field=models.BooleanField(default=False, verbose_name='подписчик'),
        ),
        migrations.AddField(
            model_name='profile',
            name='pay_cnt',
            field=models.IntegerField(default=0, verbose_name='попытки списания'),
        ),
    ]
