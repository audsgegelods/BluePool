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
        
        if ride.pick_up_lat and ride.pick_up_lng and ride.pick_up_lng and ride.drop_off_lat and ride.drop_off_location and ride.drop_off_id != None:
            pick_up_lat = ride.pick_up_lat
            pick_up_lng = ride.pick_up_lng
            pick_up_id = ride.pick_up_id
            
            drop_off_lat = ride.drop_off_lat
            drop_off_lng = ride.drop_off_lng
            drop_off_id = ride.drop_off_id
            label = "from db"
        
        elif ride.pick_up_location and ride.drop_off_location != None:
            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
            
            pick_up = gmaps.geocode(ride.pick_up_location)[0]
            pick_up_lat = pick_up.get('geometry', {}).get('location',{}).get('lat', None)
            pick_up_lng = pick_up.get('geometry', {}).get('location',{}).get('lng', None)
            pick_up_id = pick_up.get('place_id',{})
            
            drop_off = gmaps.geocode(ride.drop_off_location)[0]
            drop_off_lat = drop_off.get('geometry', {}).get('location',{}).get('lat', None)
            drop_off_lng = drop_off.get('geometry', {}).get('location',{}).get('lng', None)
            drop_off_id = drop_off.get('place_id',{})
            
            ride.pick_up_lat = pick_up_lat
            ride.pick_up_lng = pick_up_lng
            ride.pick_up_id = pick_up_id
            
            ride.drop_off_lat = drop_off_lat
            ride.drop_off_lng = drop_off_lng
            ride.drop_off_id = drop_off_id
            label = "from api call"
            ride.save()
            
        else:
            pick_up_lat = ""
            pick_up_lng = ""
            pick_up_id = ""
            
            drop_off_lat = ""
            drop_off_lng = ""
            drop_off_id = ""
            label = "its so over"
            
        context = {
            'ride':ride,
            'pick_up_lat':pick_up_lat,
            'pick_up_lng':pick_up_lng,
            'pick_up_id':pick_up_id,
            'drop_off_lat':drop_off_lat,
            'drop_off_lng':drop_off_lng,
            'drop_off_id':drop_off_id,
            'label':label
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