from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Ride, RideRequest
from .forms import RideCreateForm
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator      
import googlemaps
from django.conf import settings
from django.views.generic import ListView, View, CreateView, UpdateView

# Create your views here.
class RideListView(LoginRequiredMixin, ListView): 
    #displays all the rides in the ride_list
    model = Ride
    template_name = 'ride_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ride_list'] = Ride.objects.all()
        return context

class RideView(LoginRequiredMixin, View):
    #displays details of a specific ride
    model = Ride
    template_name = 'ride_detail.html'
    
    def get(self, request, pk):
        ride = get_object_or_404(Ride, pk=pk) 
        GOOGLE_API_KEY = settings.GOOGLE_API_KEY

        is_driver = (ride.driver == request.user)

        pending_requests = None
        if is_driver:
            pending_requests = ride.requests.filter(status=RideRequest.PENDING)

        user_request = None
        try:
            user_request = RideRequest.objects.get(ride=ride, passenger=request.user)
        except RideRequest.DoesNotExist:
            pass

        accepted_passengers = ride.requests.filter(status=RideRequest.ACCEPTED).select_related('passenger')
            
        context = {
            'ride':ride,
            'GOOGLE_API_KEY':GOOGLE_API_KEY
            'is_driver': is_driver,
            'pending_requests': pending_requests,
            'user_request': user_request,
            'accepted_passengers': accepted_passengers,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        ride = get_object_or_404(Ride, pk=pk)
        if 'join' in request.POST:
            if ride.driver == request.user:
                messages.error(request, "You cannot request your own ride.")
                return redirect('rideposting:ride_detail', pk=ride.pk)

            RideRequest.objects.get_or_create(
                ride=ride,
                passenger=request.user,
                defaults={'status': RideRequest.PENDING}
            )
            messages.success(request, "Your request to join has been sent.")
        return redirect('rideposting:ride_detail', pk=ride.pk)

class RideCreateView(LoginRequiredMixin, CreateView):
    #creates a new ride
    model = Ride
    form_class = RideCreateForm
    template_name = 'ride_create.html'

    def form_valid(self, form):
        form.instance.driver = self.request.user
        return super().form_valid(form)
    
class RideUpdateView(UpdateView):
    #currently not implemented
    model = Ride
    #form = RideCreateForm

class HandleRideRequestView(LoginRequiredMixin, UserPassesTestMixin, View):
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def test_func(self):
        request_id = self.request.POST.get('request_id')
        ride_request = get_object_or_404(RideRequest, id=request_id)
        return ride_request.ride.driver == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to do that.")
        return redirect('rideposting:ride_list')

    def post(self, request, *args, **kwargs):
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        ride_request = get_object_or_404(RideRequest, id=request_id)

        if action == 'accept':
            ride_request.status = RideRequest.ACCEPTED
            messages.success(request, f"Accepted {ride_request.passenger.username}.")
        elif action == 'reject':
            ride_request.status = RideRequest.REJECTED
            messages.success(request, f"Rejected {ride_request.passenger.username}.")
        else:
            messages.error(request, "Invalid action.")
            return redirect('rideposting:ride_detail', pk=ride_request.ride.pk)

        ride_request.save()
        return redirect('rideposting:ride_detail', pk=ride_request.ride.pk)