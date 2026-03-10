from django.test import TestCase
from django.utils import timezone
from .models import Ride

# Create your tests here.
class RideTests(TestCase):
    def testRide(self):
        sampleRide = Ride.objects.create(time = timezone.now(), pick_up_location = "here", drop_off_location = "there")
        self.assertTrue(isinstance(sampleRide,Ride))
        # self.assertEqual(sampleRide.time, timezone.now())
        self.assertEqual(sampleRide.pick_up_location, "here")
        self.assertEqual(sampleRide.drop_off_location, "there")