from rest_framework import serializers
from .models import Ride, RideRequest
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class RideRequestSerializer(serializers.ModelSerializer):
    passenger = UserBriefSerializer(read_only=True)

    class Meta:
        model = RideRequest
        fields = ['id', 'passenger', 'status', 'created_at', 'updated_at']

class RideSerializer(serializers.ModelSerializer):
    driver = UserBriefSerializer(read_only=True)
    requests = RideRequestSerializer(many=True, read_only=True)
    accepted_passengers = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            'id', 'pick_up_time', 'pick_up_location', 'drop_off_location',
            'route', 'driver', 'requests', 'accepted_passengers'
        ]
        read_only_fields = ['driver']

    def get_accepted_passengers(self, obj):
        accepted = obj.requests.filter(status=RideRequest.ACCEPTED)
        return UserBriefSerializer([req.passenger for req in accepted], many=True).data