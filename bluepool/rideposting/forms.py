from django import forms
from .models import Ride

class RideCreateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pick_up_location', 'drop_off_location']
        widgets = {
            'time': forms.TextInput(attrs={'type': 'datetime-local'}),
        }