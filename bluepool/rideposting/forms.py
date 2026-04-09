from django import forms
from .models import Ride, Message

class RideCreateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pick_up_location', 'drop_off_location', 'pick_up_time']
        widgets = {
            #'time': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Aa', 'class': 'p-4 text-black', 'maxlength': '300', 'autofocus': True})
        }