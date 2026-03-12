from django.shortcuts import redirect, render
from .models import Ride
from .forms import RideCreateForm
import googlemaps
from django.conf import settings
from django.views.generic import ListView, View, CreateView, UpdateView

# Create your views here.
class RideListView(ListView): 
    #displays all the rides in the ride_list
    model = Ride
    template_name = 'ride_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ride_list'] = Ride.objects.all()
        return context

class RideView(View):
    #displays details of a specific ride
    model = Ride
    template_name = 'ride_detail.html'
    
    def get(self, request, pk):
        ride = Ride.objects.get(pk=pk)
        GOOGLE_API_KEY = settings.GOOGLE_API_KEY
            
        context = {
            'ride':ride,
            'GOOGLE_API_KEY':GOOGLE_API_KEY
        }
        
        return render(request, self.template_name, context)
        


class RideCreateView(CreateView):
    #creates a new ride
    model = Ride
    form_class = RideCreateForm
    template_name = 'ride_create.html'
    
class RideUpdateView(UpdateView):
    #currently not implemented
    model = Ride
    #form = RideCreateForm