from django.urls import path
from .views import SmartBookingView, RoomBookingListView, BookedDatesView, BathOrBBQZoneBookingView

urlpatterns = [
    path('rooms/book/', SmartBookingView.as_view()),
    path('rooms/bookings/', RoomBookingListView.as_view()),
    path('booked-dates/', BookedDatesView.as_view(), name='booked-dates'),
    path('bathbbq/book/', BathOrBBQZoneBookingView.as_view(), name='bathbbq-booking'),
]
