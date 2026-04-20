from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Ride, RideRequest
from .serializers import RideSerializer, RideRequestSerializer

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
        serializer.save(driver=self.request.user)

class RideRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

class JoinRideAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        ride = get_object_or_404(Ride, pk=pk)
        if ride.driver == request.user:
            return Response({'error': 'You cannot join your own ride'}, status=400)
        req, created = RideRequest.objects.get_or_create(
            ride=ride, passenger=request.user,
            defaults={'status': RideRequest.PENDING}
        )
        if not created:
            return Response({'error': 'Request already exists'}, status=400)
        return Response({'status': 'pending'}, status=201)

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