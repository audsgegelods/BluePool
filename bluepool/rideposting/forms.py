from django import forms
from .models import Ride

class RideCreateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['pick_up_location', 'drop_off_location', 'pick_up_time']
        widgets = {
            'pick_up_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }