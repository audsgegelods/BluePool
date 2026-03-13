from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from rideposting.models import Ride, RideRequest
from user_management.models import Profile
import googlemaps

# Create your tests here.
class TestRides(TestCase):
    # def setUp(self):
    #     self.userD = User.objects.create_user(username="drive", email="drive@student.ateneo.edu", password="poster")
    #     self.userR = User.objects.create_user(username="ride", email="ride@student.ateneo.edu", password="applicant")
    #     driver = Profile.objects.create(user = self.userD, name = "drive", email_address = "drive@student.ateneo.edu")
    #     rider = Profile.objects.create(user = self.userR, name = "rider", email_address = "ride@student.ateneo.edu")
    #     self.client = Client()
    
    def test_ride_pu_loc(self):
        time = timezone.now()
        ride = Ride.objects.create(pick_up_time = time, pick_up_location = 'UP Town Center', drop_off_location =  'Ateneo de Manila University')
        self.assertEqual(ride.pick_up_location, 'UP Town Center')

    def test_ride_do_loc(self):
        time = timezone.now()
        ride = Ride.objects.create(pick_up_time = time, pick_up_location = 'UP Town Center', drop_off_location =  'Ateneo de Manila University')
        self.assertEqual(ride.drop_off_location, 'Ateneo de Manila University')

    def test_ride_time(self):
        time = timezone.now()
        ride = Ride.objects.create(pick_up_time = time, pick_up_location = 'UP Town Center', drop_off_location =  'Ateneo de Manila University')
        self.assertEqual(ride.pick_up_time, time)
        
    def test_valid_API_key(self):
        gmaps = googlemaps.Client(settings.GOOGLE_API_KEY)
        self.assertIsInstance(gmaps, googlemaps.Client)

    def test_invalid_API_key(self):
        with self.assertRaisesMessage(ValueError, "Invalid API key provided."):googlemaps.Client('INVALID KEY')