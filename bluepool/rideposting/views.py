from django.contrib import messages 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Ride, RideRequest, Message
from .forms import RideCreateForm, MessageCreateForm
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator      
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

class RideView(LoginRequiredMixin, View):
    #displays details of a specific ride
    model = Ride
    template_name = 'ride_detail.html'
    
    def get(self, request, pk):
        ride = get_object_or_404(Ride, pk=pk) 
        GOOGLE_API_KEY = settings.GOOGLE_API_KEY
        form = MessageCreateForm()

        is_driver = (ride.driver == request.user)

        pending_requests = None
        if is_driver:
            pending_requests = ride.requests.filter(status=RideRequest.PENDING)

        user_request = None
        try:
            user_request = RideRequest.objects.get(ride=ride, passenger=request.user)
        except RideRequest.DoesNotExist:
            pass

        try:
            messages = ride.chat.all()
        except RideRequest.DoesNotExist:
            pass

        accepted_passengers = ride.requests.filter(status=RideRequest.ACCEPTED).select_related('passenger')
        
        selfUrl = request.path
            
        context = {
            'ride':ride,
            'GOOGLE_API_KEY':GOOGLE_API_KEY,
            'is_driver': is_driver,
            'pending_requests': pending_requests,
            'user_request': user_request,
            'accepted_passengers': accepted_passengers,
            'messages': messages,
            'msgForm': form,
            'page': selfUrl
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        ride = get_object_or_404(Ride, pk=pk)
        if request.method == 'POST':
            if request.POST['form_id'] == 'apply':
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
            # elif request.htmx:
            else:
                form = MessageCreateForm(request.POST)
                if form.is_valid:
                    message = form.save(commit=False)
                    message.author = request.user
                    message.ride = ride
                    message.save()
                    formContext = {
                        'message' : message,
                        'user' : request.user,
                    }
                    return redirect('rideposting:ride_detail', pk=ride.pk)
                    # return render(request, 'partials/chatbox_p.html', formContext)
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