# Generated by Django 3.2 on 2021-04-24 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_app', '0005_auto_20210424_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='purchased_seats',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
