from django.contrib import admin
from .models import Ride


class RideInline(admin.StackedInline):
    model = Ride
    can_delete = False


class RideAdmin(admin.ModelAdmin):
    model = Ride
    can_delete = False

admin.site.register(Ride, RideAdmin)
