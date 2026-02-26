from django.urls import path

from .views import RideListView, RideDetailView, RideCreateView, RideUpdateView

urlpatterns= [
    path('rides', RideListView.as_view(), name='ride_list'),
    path('ride/<int:pk>', RideDetailView.as_view(), name='ride_detail'),
    path('ride/add', RideCreateView.as_view(), name='ride_create'),
    path('ride/<int:pk>/edit', RideUpdateView.as_view(), name='ride_update')
]

app_name = "rideposting"
