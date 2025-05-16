from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class BathOrBBQZone(models.Model):
    ZONE_TYPES = [
        ('bath', 'Баня'),
        ('bbq', 'Барбекю'),
    ]
    zone_type = models.CharField(max_length=10, choices=ZONE_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bathbbq_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.get_zone_type_display()} — {self.name}"


class EntertainmentZone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='entertainment_images/', null=True, blank=True)

    def __str__(self):
        return f"Развлечение — {self.name}"

class Room(models.Model):
    CATEGORY_CHOICES = [
        ('lux', 'Люкс'),
        ('standard', 'Стандарт'),
        ('group', 'Групповое размещение'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='standard')
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return self.name
