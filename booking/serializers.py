from rest_framework import serializers
from .models import RoomBooking, ZoneBooking

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = '__all__'
