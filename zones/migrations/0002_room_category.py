# Generated by Django 5.2 on 2025-05-08 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='category',
            field=models.CharField(choices=[('lux', 'Люкс'), ('standard', 'Стандарт'), ('group', 'Групповое размещение')], default='standard', max_length=20),
        ),
    ]
