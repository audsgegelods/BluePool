from django.contrib import admin
from .models import Ride, Message


class RideInline(admin.StackedInline):
    model = Ride
    can_delete = False


class RideAdmin(admin.ModelAdmin):
    model = Ride
    can_delete = False


class MessageInline(admin.StackedInline):
    model = Message
    can_delete = False


class MessageAdmin(admin.ModelAdmin):
    model = Message
    can_delete = False

admin.site.register(Ride, RideAdmin)
admin.site.register(Message, MessageAdmin)
