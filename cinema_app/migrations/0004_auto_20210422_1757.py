# Generated by Django 3.2 on 2021-04-22 14:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_app', '0003_auto_20210422_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
