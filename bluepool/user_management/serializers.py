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
        fields = ["id", "username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}   # do not return password when requesting user data

        def create(self, validated_data):
            email_address = validated_data["email"]
            new_user = User.objects.create_user(
                username=validated_data.get("username", ""),
                email=email_address,
                first_name=validated_data.get("first_name", ""),
                last_name=validated_data.get("last_name", ""),
                password=validated_data["password"]
            )
            # new_profile = Profile.objects.create(
            #     user=new_user,
            #     name=validated_data.get("username", None),
            #     email_address=validated_data.get("email", None))
            # new_profile.save()
            return new_user

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields