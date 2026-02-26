from django.shortcuts import redirect
from .models import Ride
from .forms import RideCreateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView

# Create your views here.
class RideListView(ListView): 
    #displays all the rides in the ride_list
    model = Ride
    template_name = 'ride_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ride_list'] = Ride.objects.all()
        return context

class RideDetailView(DetailView):
    #displays details of a specific ride
    model = Ride
    template_name = 'ride_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class RideCreateView(CreateView):
    #creates a new ride
    model = Ride
    form_class = RideCreateForm
    template_name = 'ride_create.html'
    
class RideUpdateView(UpdateView):
    #currently not implemented
    model = Ride
    #form = RideCreateForm