# Generated by Django 4.2.2 on 2023-06-30 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot_app', '0010_flightsubscription_is_direct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flightsubscription',
            old_name='arrival_date',
            new_name='return_date',
        ),
    ]
