from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from pytz import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from ..models import Listing, Room, Reservation
from ..serializers import ListingSerializer, RoomSerializer, ReservationSerializer
import datetime
import json


class ListingViewTestCase(APITestCase):
    """
    it tests the GET method for retrieving all listings and asserts that the
    response data equals the serialized data retrieved from the database.
    """
    def setUp(self):
        self.client = Client()
        self.listing = Listing.objects.create(name="Test Listing")
        self.listing2 = Listing.objects.create(name="Test Listing 2")
    
    def test_get_all_listings(self):
        response = self.client.get(reverse('listing-list'))
        listings = Listing.objects.all()
        serializer = ListingSerializer(listings, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoomViewTestCase(APITestCase):
    """
    it tests the GET method for retrieving all rooms and asserts that the response
    data equals the serialized data retrieved from the database.
    """
    def setUp(self):
        self.client = Client()
        self.listing = Listing.objects.create(name="Test Listing")
        self.room = Room.objects.create(name="Test Room", listing=self.listing, capacity=5)
        self.room2 = Room.objects.create(name="Test Room 2", listing=self.listing, capacity=3)
    
    def test_get_all_rooms(self):
        response = self.client.get(reverse('room-list'))
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class MakeReservationViewTestCase(APITestCase):
    """
    it tests the POST method for creating a new reservation for a room
    and asserts that the response status code is HTTP 201 (Created).
    """
    def setUp(self):
        self.client = Client()
        self.listing = Listing.objects.create(name="Test Listing")
        self.room = Room.objects.create(name="Test Room", listing=self.listing, capacity=5)
    
    def test_make_reservation(self):
        data = {
            'name': 'Test Reservation',
            'room': self.room.id,
            'start_time': datetime.datetime.now(),
            'end_time': datetime.datetime.now() + datetime.timedelta(hours=2)
        }
        response = self.client.post(reverse('make-reservation'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class CheckAvailabilityViewTestCase(TestCase):
    """
    it tests the GET method for checking if a room is available for
    a given time period and asserts that the response data equals {"available": True} if the room is available, or {"error": "start_time and end_time parameters are required"} if the request parameters are invalid.
    """
    def setUp(self):
        self.client = APIClient()
        self.listing = Listing.objects.create(name='Test Listing')
        self.room = Room.objects.create(
            listing=self.listing,
            name='Test Room',
            capacity=2
        )

    def test_check_availability_valid_params(self):
        start_time = datetime.now(tz=timezone('UTC')) + timedelta(days=1)
        end_time = start_time + timedelta(days=1)
        url = reverse('check-availability', kwargs={'name': self.room.name})
        response = self.client.get(url, {'start_time': start_time.isoformat(), 'end_time': end_time.isoformat()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'available': True})

    def test_check_availability_invalid_params(self):
        url = reverse('check-availability', kwargs={'name': self.room.name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'start_time and end_time parameters are required'})


class OverviewReportTestCase(TestCase):
    """
    it tests the GET method for retrieving an overview report for all reservations
    and asserts that the response data is correctly rendered in either HTML or plain text format.
    """
    def setUp(self):
        self.client = APIClient()
        self.listing = Listing.objects.create(name='Test Listing')
        self.room = Room.objects.create(
            listing=self.listing,
            name='Test Room',
            capacity=2
        )
        self.reservation = Reservation.objects.create(
            room=self.room,
            name='Test Reservation',
            start_time=datetime.now(tz=timezone('UTC')) + timedelta(days=1),
            end_time=datetime.now(tz=timezone('UTC')) + timedelta(days=2)
        )

    def test_overview_report_html(self):
        url = reverse('overview-report')
        response = self.client.get(url, {'HTTP_ACCEPT': 'text/html'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.reservation.name)

    def test_overview_report_text(self):
        url = reverse('overview-report')
        response = self.client.get(url, {'HTTP_ACCEPT': 'text/plain'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.reservation.name, response.content.decode())