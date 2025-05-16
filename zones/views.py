from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Room, BathOrBBQZone, EntertainmentZone
from .serializers import RoomSerializer, BathOrBBQZoneSerializer, EntertainmentZoneSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from booking.models import RoomBooking
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RoomCreateView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

class RoomUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

class AvailableRoomsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')
        if not check_in or not check_out:
            return Response({'error': 'check_in и check_out обязательны'}, status=400)
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        booked_rooms = RoomBooking.objects.filter(check_in__lt=check_out_date, check_out__gt=check_in_date).values_list('room_id', flat=True)
        available_rooms = Room.objects.exclude(id__in=booked_rooms)
        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data)

class BathOrBBQZoneListCreateView(ListCreateAPIView):
    queryset = BathOrBBQZone.objects.all()
    serializer_class = BathOrBBQZoneSerializer
    permission_classes = [IsAdminOrReadOnly]

class BathOrBBQZoneDetailView(RetrieveUpdateDestroyAPIView):
    queryset = BathOrBBQZone.objects.all()
    serializer_class = BathOrBBQZoneSerializer
    permission_classes = [IsAdminOrReadOnly]

class EntertainmentZoneListCreateView(ListCreateAPIView):
    queryset = EntertainmentZone.objects.all()
    serializer_class = EntertainmentZoneSerializer
    permission_classes = [IsAdminOrReadOnly]

class EntertainmentZoneDetailView(RetrieveUpdateDestroyAPIView):
    queryset = EntertainmentZone.objects.all()
    serializer_class = EntertainmentZoneSerializer
    permission_classes = [IsAdminOrReadOnly]