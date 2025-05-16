from rest_framework import serializers
from .models import RoomBooking

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = '__all__'
