from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Ride, RideRequest, Message
from .serializers import RideSerializer, MessageSerializer
from .forms import MessageCreateForm
import googlemaps
from django.conf import settings

class RideListAPIView(generics.ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Ride.objects.all()
        
        # filter parameters
        pick_up = self.request.query_params.get('pick_up_location')
        drop_off = self.request.query_params.get('drop_off_location')
        
        # apply filters
        if pick_up:
            queryset = queryset.filter(pick_up_location__icontains=pick_up)
        if drop_off:
            queryset = queryset.filter(drop_off_location__icontains=drop_off)
        
        return queryset.order_by('pick_up_time')

class RideCreateAPIView(generics.CreateAPIView):
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        pick_up = gmaps.find_place(serializer.validated_data['pick_up_location'], input_type="textquery")
        pick_up_place = gmaps.place(pick_up.get("candidates",{})[0].get("place_id", None))
        drop_off = gmaps.find_place(serializer.validated_data['drop_off_location'], input_type="textquery")
        drop_off_place = gmaps.place(drop_off.get("candidates",{})[0].get("place_id", None))
        
        pick_up_parts = [pick_up_place["result"]["name"],pick_up_place["result"]["formatted_address"]]
        drop_off_parts = [drop_off_place["result"]["name"],drop_off_place["result"]["formatted_address"]]
        
        if pick_up_parts[0] == None:
            pick_up_parts[0] = serializer.validated_data['pick_up_location'].title()
        if drop_off_parts[0] == None:
            drop_off_parts[0] = serializer.validated_data['drop_off_location'].title()
        
        pick_up_result = pick_up_parts[0] + ", " + pick_up_parts[1]
        drop_off_result = drop_off_parts[0] + ", " + drop_off_parts[1]
        
        result = gmaps.distance_matrix(pick_up_result, drop_off_result, mode="driving")
        
        final = result.get("rows", [])[0].get("elements", [])[0].get("duration", {}).get("text", None)
        serializer.save(route=final, pick_up_location=pick_up_result, drop_off_location=drop_off_result, driver=self.request.user)

class RideRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

class JoinRideAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        form = MessageCreateForm()
        return Response(form)

    def post(self, request, pk):
        ride = get_object_or_404(Ride, pk=pk)
        if request.method == 'POST':
            form_id = request.POST.get("form_id")
            if form_id == "send":
                form = MessageCreateForm(request.POST)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.author = request.user
                    message.ride = get_object_or_404(Ride, pk=pk)
                    message.save()

                    if request.headers.get("HX-Request"):
                        return Response(request, {
                            'message': message,
                            'user': request.user,
                        })
                    
        if ride.driver == request.user:
            return Response({'error': 'You cannot join your own ride'}, status=400)
        req, created = RideRequest.objects.get_or_create(
            ride=ride, passenger=request.user,
            defaults={'status': RideRequest.PENDING}
        )
        if not created:
            return Response({'error': 'Request already exists'}, status=400)
    
        return Response({'status': 'pending'}, status=201)


class MessagesAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     queryset = Message.objects.all()
    #     return queryset.order_by('time')

    def get_ride_permission(self):
        ride_id = self.kwargs.get('ride_id')
        ride = get_object_or_404(Ride, pk=ride_id)
        user = self.request.user

        if ride.driver == user:
            return ride

    def get_queryset(self):
        ride = self.get_ride_permission()
        return Message.objects.filter(ride=ride).order_by('time')

    def perform_create(self, serializer):
        ride = self.get_ride_permission()
        serializer.save(author=self.request.user, ride=ride)

class HandleRideRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        req_id = request.data.get('request_id')
        action = request.data.get('action')
        ride_req = get_object_or_404(RideRequest, id=req_id)
        if ride_req.ride.driver != request.user:
            return Response({'error': 'Not your ride'}, status=403)
        if action == 'accept':
            ride_req.status = RideRequest.ACCEPTED
        elif action == 'reject':
            ride_req.status = RideRequest.REJECTED
        else:
            return Response({'error': 'Invalid action'}, status=400)
        ride_req.save()
        return Response({'status': ride_req.status})