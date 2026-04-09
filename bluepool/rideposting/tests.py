from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from rideposting.models import Ride, RideRequest, Message
from rideposting.forms import RideCreateForm, MessageCreateForm
from user_management.models import Profile
import googlemaps

# Create your tests here.
class TestRides(TestCase):
    def setUp(self):
        self.userD = User.objects.create_user(username="drive", email="drive@student.ateneo.edu", password="poster")
        self.userR = User.objects.create_user(username="ride", email="ride@student.ateneo.edu", password="applicant")
        self.driver = Profile.objects.create(user = self.userD, name = "drive", email_address = "drive@student.ateneo.edu")
        self.rider = Profile.objects.create(user = self.userR, name = "rider", email_address = "ride@student.ateneo.edu")
        self.client = Client()
    
    def test_ride_add_form(self):
        time = timezone.now()
        form = RideCreateForm(data = {
            'pick_up_location': 'UP Diliman', 
            'drop_off_location': 'Ateneo de Manila University', 
            'pick_up_time' : time
        })
        self.assertTrue(form.is_valid())

    def test_ride_is_posted(self):
        time = timezone.now()
        self.client.post("/account/login/", {"username": "drive", "password" : "poster"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "UP Town Center", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        self.assertTrue(Ride.objects.exists())

    def test_ride_ownership(self):
        time = timezone.now()
        self.client.post("/account/login/", {"username": "drive", "password" : "poster"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "UP Town Center", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        evalObj = Ride.objects.get(pick_up_location = "UP Town Center")
        self.assertEqual(evalObj.driver, self.driver.user)
        self.assertNotEqual(evalObj.driver, self.rider.user)
        self.client.logout()

        self.client.post("/account/login/", {"username": "ride", "password" : "applicant"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "Zu's Coffee", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        evalObjB = Ride.objects.get(pick_up_location = "Zu's Coffee")
        self.assertEqual(evalObjB.driver, self.rider.user)
        self.assertNotEqual(evalObjB.driver, self.driver.user)
        
    def test_passenger_can_request_ride(self):
        time = timezone.now()
        self.client.post("/account/login/", {"username": "drive", "password" : "poster"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "UP Town Center", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        self.client.logout()
        self.client.post("/account/login/", {"username": "ride", "password" : "applicant"})
        self.client.post("/rideposting/ride/1", {"form_id": "apply"})
        self.assertTrue(RideRequest.objects.exists())
        
    def test_driver_cannot_request_own_ride(self):
        time = timezone.now()
        self.client.post("/account/login/", {"username": "drive", "password" : "poster"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "UP Town Center", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        self.client.post("/rideposting/ride/1", {"form_id": "apply"})
        self.assertFalse(RideRequest.objects.exists())
        
    def test_unauthenticated_user_cannot_request_ride(self):
        time = timezone.now()
        self.client.post("/account/login/", {"username": "drive", "password" : "poster"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "UP Town Center", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        self.client.logout()
        response = self.client.post("/rideposting/ride/1", {"form_id": "apply"})
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RideRequest.objects.exists())
        
    def test_valid_message_form(self):
        form = MessageCreateForm(data = {
            'text': 'Hello World'
        })
        self.assertTrue(form.is_valid())
    
    def test_post_message(self):
        time = timezone.now()
        self.client.post("/account/login/", {"username": "drive", "password" : "poster"})
        self.client.post("/rideposting/ride/add", {"pick_up_location": "UP Town Center", "drop_off_location" : "Ateneo de Manila University", "pick_up_time" : time})
        self.client.post("/rideposting/ride/1", {"form_id": "send", "text": 'Hello World', 'user': self.driver.user, 'ride': Ride.objects.get(id=1)})
        self.assertTrue(Message.objects.exists())
    
    # def test_