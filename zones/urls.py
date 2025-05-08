from django.urls import path
from .views import (
    RoomListView, ZoneListView, RoomCreateView, ZoneCreateView,
    RoomUpdateDeleteView, ZoneUpdateDeleteView,
    AvailableRoomsView, AvailableZonesView
)

urlpatterns = [
    path('rooms/', RoomListView.as_view()),
    path('zones/', ZoneListView.as_view()),
    path('rooms/create/', RoomCreateView.as_view()),
    path('zones/create/', ZoneCreateView.as_view()),
    path('rooms/<int:pk>/', RoomUpdateDeleteView.as_view()),
    path('zones/<int:pk>/', ZoneUpdateDeleteView.as_view()),
    path('rooms/available/', AvailableRoomsView.as_view()),
    path('zones/available/', AvailableZonesView.as_view()),
]
