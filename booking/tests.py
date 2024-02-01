from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import Room, Booking


# Create your tests here.
class RoomBookingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='humoyunswe', password='1234')
        self.room = Room.objects.create(title='CoWorking', capacity=20, description="Room for co-working!")
        self.booking = Booking.objects.create(room=self.room, customer=self.user, checking_date=timezone.now(), checkout_date=timezone.now())

    def test_rooms(self):
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('available', response.data)
        self.assertIn('reserved', response.data)
        self.assertIn('date', response.data)

    def test_for_authentication(self):
        self.client.force_authenticate(user=self.user)
        data = {'room_name': 'CoWorking', 'start': str(timezone.now().date()), 'end': str(timezone.now().date() + timedelta(days=1))}
        response = self.client.post('/api/book/room/', data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.data)
        self.assertIn('room', response.data)
        self.assertIn('room_name', response.data)
        self.assertIn('start', response.data)
        self.assertIn('end', response.data)

    def test_for_unauthentication(self):
        data = {'room_name': 'CoWorking', 'start': str(timezone.now().date()),'end': str(timezone.now().date() + timedelta(days=1))}
        response = self.client.post('/api/book/room/', data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)

    def test_room_detail(self):
        response = self.client.get('/api/room/CoWorking/')
        obj1 =  Room.objects.get(title='CoWorking', capacity=20, description="Room for co-working!")

        self.assertEqual(response.status_code, 404)
        self.assertIn(obj1.title, 'CoWorking')
        self.assertIn(obj1.capacity, [20,])
        self.assertIn(obj1.description, 'Room for co-working!')

    def test_singUp_success(self):
        data = {'username': 'Xumoyun', 'password': '1234'}
        response = self.client.post('/api/signup/', data)
        self.assertIn('message', response.data)

    def test_signup_duplicate_username(self):
        User.objects.create_user(username='testuser', password='testpassword')

        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/api/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


