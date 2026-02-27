from django.shortcuts import render
from .models import Profile
from django.views.generic.edit import UpdateView


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'profile.html'
