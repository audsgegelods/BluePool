from django.db import models
from django.urls import reverse

# Create your models here.
class Ride(models.Model):
    """
        This creates a Ride model
    """
    time = models.DateTimeField() #currently just setting the pickup time automatically to the current time gahaha
    pick_up_location = models.TextField() #todo: once map integration is implemented, change this to location based
    drop_off_location = models.TextField()
    
    route = models.CharField(max_length=200,blank=True,null=True)
    #to do: when profiles are implemented, add profile linking for both riders (many to one) and driver (one to one)
    
    def get_absolute_url(self):
        return reverse('rideposting:ride_detail', args=[str(self.pk)])