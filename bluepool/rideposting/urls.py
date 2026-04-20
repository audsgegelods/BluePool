from django.urls import path
from . import api_views

from .views import RideListView, RideView, RideCreateView, RideUpdateView, HandleRideRequestView

urlpatterns= [
    path('rides', RideListView.as_view(), name='ride_list'),
    path('ride/<int:pk>', RideView.as_view(), name='ride_detail'),
    path('ride/add', RideCreateView.as_view(), name='ride_create'),
    path('ride/<int:pk>/edit', RideUpdateView.as_view(), name='ride_update'),
    path('handle-request/', HandleRideRequestView.as_view(), name='handle_request'),
   
    # new paths
    path('api/rides/', api_views.RideListAPIView.as_view(), name='api_ride_list'),
    path('api/ride/add/', api_views.RideCreateAPIView.as_view(), name='api_ride_create'),
    path('api/ride/<int:pk>/', api_views.RideRetrieveUpdateDestroyAPIView.as_view(), name='api_ride_detail'),
    path('api/ride/<int:pk>/join/', api_views.JoinRideAPIView.as_view(), name='api_ride_join'),
    path('api/handle-request/', api_views.HandleRideRequestAPIView.as_view(), name='api_handle_request')
]

app_name = "rideposting"
