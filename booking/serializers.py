from rest_framework import serializers
from .models import RoomBooking, ZoneBooking

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = '__all__'

class ZoneBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneBooking
        fields = '__all__'
