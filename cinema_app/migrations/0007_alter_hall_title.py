# Generated by Django 3.2 on 2021-04-24 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_app', '0006_session_purchased_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
