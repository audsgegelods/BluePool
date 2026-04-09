from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}   # do not return password when requesting user data

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            new_profile = Profile(
                user=User.objects.get(username=validated_data['username']),
                name=validated_data['display_name'],
                email_address=validated_data['email']
            )
    
            return user