from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room
from .models import BathOrBBQZone, EntertainmentZone

admin.site.register(Room)
admin.site.register(BathOrBBQZone)
admin.site.register(EntertainmentZone)