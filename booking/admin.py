from django.contrib import admin
from .models import RoomBooking, BathOrBBQZoneBooking  

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'name', 'check_in', 'check_out', 'created_at')
    list_filter = ('room', 'check_in', 'check_out')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)

@admin.register(BathOrBBQZoneBooking)
class BathOrBBQZoneBookingAdmin(admin.ModelAdmin):
    list_display = ('zone', 'name', 'booking_date', 'hours', 'created_at')  
    list_filter = ('zone', 'booking_date')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)
