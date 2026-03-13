from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from rideposting.models import Ride
from rideposting.forms import RideCreateForm
from user_management.models import Profile
import googlemaps

# Create your tests here.
class TestRides(TestCase):
    def setUp(self):
        self.userD = User.objects.create_user(username="drive", email="drive@student.ateneo.edu", password="poster")
        self.userR = User.objects.create_user(username="ride", email="ride@student.ateneo.edu", password="applicant")
        driver = Profile.objects.create(user = self.userD, name = "drive", email_address = "drive@student.ateneo.edu")
        rider = Profile.objects.create(user = self.userR, name = "rider", email_address = "ride@student.ateneo.edu")
        self.client = Client()
    
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
    
    def test_ride_add_form(self):
        time = timezone.now()
        form = RideCreateForm(data = {
            'pick_up_location': 'UP Diliman', 
            'drop_off_location': 'Ateneo de Manila University', 
            'pick_up_time' : time
        })
        self.assertTrue(form.is_valid())

    def test_ride_ownership(self):
        time = timezone.now()
        self.client.post("/account/login/", {"username": "drive", "password" : "poster"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "UP Town Center", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        evalObj = Ride.objects.get(pick_up_location = "UP Town Center")
        self.assertEqual(evalObj.driver, self.userD)
        self.assertNotEqual(evalObj.driver, self.userR)
        self.client.logout()

        self.client.post("/account/login/", {"username": "ride", "password" : "applicant"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "Zu's Coffee", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        evalObjB = Ride.objects.get(pick_up_location = "Zu's Coffee")
        self.assertEqual(evalObjB.driver, self.userR)
        self.assertNotEqual(evalObjB.driver, self.userD)