from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Zone

admin.site.register(Room)
admin.site.register(Zone)
