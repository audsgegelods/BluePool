from django.db import models
from django.contrib.auth.models import User


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=63)
    lname = models.CharField(max_length=63)
    email_address = models.EmailField()
