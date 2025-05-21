from rest_framework import serializers
from .models import RoomBooking, BathOrBBQZoneBooking

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = '__all__'

class BathOrBBQZoneBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BathOrBBQZoneBooking
        fields = '__all__'