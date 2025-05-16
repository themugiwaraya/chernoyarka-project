from django.db import models
from zones.models import Room

# Create your models here.
class RoomBooking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
    ('pending', 'Ожидает'),
    ('confirmed', 'Подтверждено'),
    ('canceled', 'Отменено'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.name} — {self.room.name} с {self.check_in} по {self.check_out}"

