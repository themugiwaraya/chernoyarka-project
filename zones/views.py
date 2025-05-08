from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Room, Zone
from .serializers import RoomSerializer, ZoneSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from booking.models import RoomBooking, ZoneBooking
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ZoneListView(ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RoomCreateView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

class ZoneCreateView(CreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAdminOrReadOnly]

class RoomUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

class ZoneUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
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

class AvailableZonesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        booking_date = request.GET.get('date')
        if not booking_date:
            return Response({'error': 'date обязателен'}, status=400)
        date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
        booked_zones = ZoneBooking.objects.filter(booking_date=date_obj).values_list('zone_id', flat=True)
        available_zones = Zone.objects.exclude(id__in=booked_zones)
        serializer = ZoneSerializer(available_zones, many=True)
        return Response(serializer.data)
