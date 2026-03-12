from django.db import models
from django.conf import settings  
from django.urls import reverse

# Create your models here.
class Ride(models.Model):
    """
        This creates a Ride model
    """
    pick_up_time = models.DateTimeField() #currently just setting the pickup time automatically to the current time gahaha
    pick_up_location = models.TextField() #todo: once map integration is implemented, change this to location based
    drop_off_location = models.TextField()
    
    route = models.CharField(max_length=200,blank=True,null=True)
    #to do: when profiles are implemented, add profile linking for both riders (many to one) and driver (one to one)
    
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='driven_rides',
        null=True
    )

    passengers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='RideRequest',
        related_name='rides_as_passenger' 
    )

    def get_absolute_url(self):
        return reverse('rideposting:ride_detail', args=[str(self.pk)])
    
class RideRequest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ride_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['ride', 'passenger']

    def __str__(self):
        return f"{self.passenger} - {self.ride} ({self.status})"
