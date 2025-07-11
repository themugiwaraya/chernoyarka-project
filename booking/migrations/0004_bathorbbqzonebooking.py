# Generated by Django 5.2 on 2025-05-21 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_delete_zonebooking'),
        ('zones', '0003_bathorbbqzone_entertainmentzone_delete_zone'),
    ]

    operations = [
        migrations.CreateModel(
            name='BathOrBBQZoneBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('booking_date', models.DateField()),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zones.bathorbbqzone')),
            ],
        ),
    ]
