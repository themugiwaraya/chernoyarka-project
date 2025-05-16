from django.urls import path
from .views import (
    RoomListView, RoomCreateView,
    RoomUpdateDeleteView, AvailableRoomsView,
    BathOrBBQZoneListCreateView, BathOrBBQZoneDetailView,
    EntertainmentZoneListCreateView, EntertainmentZoneDetailView
)

urlpatterns = [
    path('rooms/', RoomListView.as_view()),
    path('rooms/create/', RoomCreateView.as_view()),
    path('rooms/<int:pk>/', RoomUpdateDeleteView.as_view()),
    path('rooms/available/', AvailableRoomsView.as_view()),
    path('zones/bath-bbq/', BathOrBBQZoneListCreateView.as_view(), name='bathbbqzone-list-create'),
    path('zones/bath-bbq/<int:pk>/', BathOrBBQZoneDetailView.as_view(), name='bathbbqzone-detail'),
    path('zones/entertainment/', EntertainmentZoneListCreateView.as_view(), name='entertainmentzone-list-create'),
    path('zones/entertainment/<int:pk>/', EntertainmentZoneDetailView.as_view(), name='entertainmentzone-detail'),
]
