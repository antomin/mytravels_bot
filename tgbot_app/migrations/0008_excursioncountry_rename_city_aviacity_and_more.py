# Generated by Django 4.2.2 on 2023-06-28 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot_app', '0007_alter_city_options_alter_country_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcursionCountry',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название')),
                ('priority', models.IntegerField(default=300, verbose_name='приоритет')),
            ],
            options={
                'verbose_name': 'страна экскурсии',
                'verbose_name_plural': 'страны экскурсии',
            },
        ),
        migrations.RenameModel(
            old_name='City',
            new_name='AviaCity',
        ),
        migrations.RenameModel(
            old_name='Country',
            new_name='AviaCountry',
        ),
        migrations.AlterModelOptions(
            name='aviacity',
            options={'ordering': ('priority', 'title'), 'verbose_name': 'город авиасейлс', 'verbose_name_plural': 'города авиасейлс'},
        ),
        migrations.AlterModelOptions(
            name='aviacountry',
            options={'ordering': ('priority', 'title'), 'verbose_name': 'страна авиасейлс', 'verbose_name_plural': 'страны авиасейлс'},
        ),
        migrations.CreateModel(
            name='ExcursionCity',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название')),
                ('priority', models.IntegerField(default=300, verbose_name='приоритет')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgbot_app.excursioncountry', verbose_name='страна')),
            ],
            options={
                'verbose_name': 'страна экскурсии',
                'verbose_name_plural': 'страны экскурсии',
            },
        ),
    ]