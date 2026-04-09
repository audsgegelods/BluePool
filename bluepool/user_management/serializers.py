from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers

# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(many=False, read_only=True)
#     class Meta:
#         model = Profile
#         fields = ["user", "name", "email_address"]
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}   # do not return password when requesting user data

        def create(self, validated_data):
            new_user = User.objects.create_user(**validated_data)
            new_profile = Profile.objects.create(
                user=new_user,
                name=validated_data.get("username", None),
                email_address=validated_data.get("email", None))
            new_profile.save()
            return new_user