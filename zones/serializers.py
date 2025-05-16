from rest_framework import serializers
from .models import Room
from .models import BathOrBBQZone, EntertainmentZone

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        
class BathOrBBQZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = BathOrBBQZone
        fields = '__all__'

class EntertainmentZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntertainmentZone
        fields = '__all__'

