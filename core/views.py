from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import render
from .models import Listing, Room, Reservation
from .serializers import ListingSerializer, RoomSerializer, ReservationSerializer


class ListingView(generics.ListAPIView):
    """
    Endpoint that lists all available listings.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class RoomView(generics.ListAPIView):
    """
    Endpoint that lists all available rooms.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MakeReservationView(generics.CreateAPIView):
    """
    Endpoint that allows a user to make a new reservation.
    """
    serializer_class = ReservationSerializer


class CheckAvailabilityView(generics.RetrieveAPIView):
    """
    Endpoint that checks if a certain room is available between a certain time range.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        room = self.get_object()
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        if not start_time or not end_time:
            return Response({'error': 'start_time and end_time parameters are required'})

        # Filter the reservations for the requested room that overlap with the requested time range
        reservations = room.reservation_set.filter(start_time__lt=end_time, end_time__gt=start_time)
        
        # Calculate the remaining capacity of the room
        capacity = room.capacity
        for reservation in reservations:
            capacity -= 1
            if capacity == 0:
                return Response({'available': False})

        # If the capacity is not reached, return available=True
        return Response({'available': True})


def overview_report(request):
    """
    Endpoint that returns an overview report of all reservations.
    """
    reservations = Reservation.objects.all()
    context = {
        'reservations': reservations
    }
    
    # Return different formats depending on the Accept header in the request
    if request.accepted_media_type == 'text/plain':
        return render(request, 'overview_report.txt', context, content_type='text/plain')
    else:
        return render(request, 'overview_report.html', context)