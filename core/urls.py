from django.urls import path
from .views import ListingView, RoomView, MakeReservationView, CheckAvailabilityView, overview_report


urlpatterns = [
    path('listings/', ListingView.as_view(), name='listing-list'),
    path('rooms/', RoomView.as_view(), name='room-list'),
    path('reservations/make/', MakeReservationView.as_view(), name='make-reservation'),
    path('reservations/check_availability/<str:name>/', CheckAvailabilityView.as_view(), name='check-availability'),
    path('reservations/overview/', overview_report, name='overview-report')
]