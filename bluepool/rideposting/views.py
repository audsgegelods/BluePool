from django.shortcuts import redirect, render
from .models import Ride
from .forms import RideCreateForm
import googlemaps
from django.conf import settings
from django.views.generic import ListView, View, CreateView, UpdateView

# Create your views here.
class RideListView(ListView): 
    model = Ride
    template_name = 'ride_list.html'
    context_object_name = 'rides'

    #displays rides based on indicated conditions
    def get_queryset(self):
        rides = Ride.objects.all()

        pick_up_loc = self.request.GET.get("pick_up_loc")
        drop_off_loc = self.request.GET.get("drop_off_loc")
        pick_up_time = self.request.GET.get("pick_up_time")

        if pick_up_loc:
            rides = rides.filter(pick_up_location=pick_up_loc)
        if drop_off_loc:
            rides = rides.filter(drop_off_location=drop_off_loc)
        if pick_up_time:
            rides = rides.filter(pick_up_time=pick_up_time)

        return rides

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