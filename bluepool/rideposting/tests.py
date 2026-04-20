from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from rideposting.models import Ride
from rideposting.forms import RideCreateForm
from user_management.models import Profile
import googlemaps

# Create your tests here.
class TestRideForm(TestCase):

    def test_valid_form(self):
        form = RideCreateForm(data={
            "pick_up_location": "UP Diliman",
            "drop_off_location": "Ateneo de Manila University",
            "pick_up_time": timezone.now() ,
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_pick_up_location_is_invalid(self):
        form = RideCreateForm(data={
            "pick_up_location": "",
            "drop_off_location": "Ateneo de Manila University",
            "pick_up_time": timezone.now() ,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("pick_up_location", form.errors)

    def test_missing_drop_off_location_is_invalid(self):
        form = RideCreateForm(data={
            "pick_up_location": "UP Diliman",
            "drop_off_location": "",
            "pick_up_time": timezone.now() ,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("drop_off_location", form.errors)

    def test_missing_pick_up_time_is_invalid(self):
        form = RideCreateForm(data={
            "pick_up_location": "UP Diliman",
            "drop_off_location": "Ateneo de Manila University",
            "pick_up_time": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("pick_up_time", form.errors)

class TestGoogleMapsClient(TestCase):

    def test_valid_api_key_creates_client(self):
        gmaps = googlemaps.Client(settings.GOOGLE_API_KEY)
        self.assertIsInstance(gmaps, googlemaps.Client)

    def test_invalid_api_key_raises_value_error(self):
        with self.assertRaises(ValueError):
            googlemaps.Client("INVALID_KEY")

    def test_empty_api_key_raises_value_error(self):
        with self.assertRaises(ValueError):
            googlemaps.Client("")


class TestRideOwnership(TestCase):

    def setUp(self):
        self.client = Client()
        self.time = timezone.now()

        self.driver_user = User.objects.create_user(
            username="driver", email="driver@student.ateneo.edu", password="secret1"
        )
        self.rider_user = User.objects.create_user(
            username="rider", email="rider@student.ateneo.edu", password="secret2"
        )
        Profile.objects.create(
            user=self.driver_user,
            name="Driver",
            email_address="driver@student.ateneo.edu",
        )
        Profile.objects.create(
            user=self.rider_user,
            name="Rider",
            email_address="rider@student.ateneo.edu",
        )        


    def post_ride(self, pick_up, drop_off):
        return self.client.post("/rideposting/ride/add",{"pick_up_location": pick_up, "drop_off_location": drop_off, "pick_up_time": self.time,})


    def test_ride_assigned_to_posting_driver(self):
        self.client.force_login(self.driver_user)
        self.post_ride("UP Town Center", "Ateneo de Manila University")

        ride = Ride.objects.get(driver=self.driver_user)
        self.assertIsNotNone(ride)

    def test_ride_not_assigned_to_other_user(self):
        self.client.force_login(self.driver_user)
        self.post_ride("UP Town Center", "Ateneo de Manila University")

        ride = Ride.objects.get(driver=self.driver_user)
        self.assertNotEqual(ride.driver, self.rider_user)

    def test_each_user_owns_their_own_ride(self):
        self.client.force_login(self.driver_user)
        self.post_ride("UP Town Center", "Ateneo de Manila University")
        self.client.logout()

        self.client.force_login(self.rider_user)
        self.post_ride("Zu's Coffee", "Ateneo de Manila University")
        self.client.logout()

        driver_ride = Ride.objects.get(driver=self.driver_user)
        rider_ride = Ride.objects.get(driver=self.rider_user)

        self.assertNotEqual(driver_ride.driver, self.rider_user)
        self.assertNotEqual(rider_ride.driver, self.driver_user)

    def test_unauthenticated_user_cannotpost_ride(self):
        self.post_ride("SM North EDSA", "Ateneo de Manila University")
        self.assertFalse(Ride.objects.filter(driver=None).exists())
        self.assertEqual(Ride.objects.count(), 0)
        
class TestRideRequestFunctionality(TestCase):
    def setUp(self):
        self.client = Client()
        self.time = timezone.now()

        def post_ride(self, pick_up, drop_off):
            return self.client.post("/rideposting/ride/add",{"pick_up_location": pick_up, "drop_off_location": drop_off, "pick_up_time": self.time,})

        self.driver_user = User.objects.create_user(
            username="driver", email="driver@student.ateneo.edu", password="secret1"
        )
        self.rider_user = User.objects.create_user(
            username="rider", email="rider@student.ateneo.edu", password="secret2"
        )
        Profile.objects.create(
            user=self.driver_user,
            name="Driver",
            email_address="driver@student.ateneo.edu",
        )
        Profile.objects.create(
            user=self.rider_user,
            name="Rider",
            email_address="rider@student.ateneo.edu",
        )
        
        self.client.force_login(self.driver_user)
        post_ride("SM North EDSA", "Ateneo de Manila University")
        
        self.ride1 = Ride.objects.get(driver=self.driver_user)
        self.client.logout()
        
        self.client.force_login(self.rider_user)
        post_ride("Zu's Coffee", "Ateneo de Manila University")
        
        self.ride2 = Ride.objects.get(driver=self.rider_user)
        self.client.logout()
        
    def test_user_can_request_to_join(self):
        self.client.force_login(self.rider_user)
        ride_url = "/rideposting/ride/" + self.ride2.id
        self.client.post(ride_url, )