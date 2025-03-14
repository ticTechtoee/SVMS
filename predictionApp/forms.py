from django import forms
from vehicleApp.models import Vehicle

class PredictionForm(forms.Form):
    vehicle_id = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        label="Select Vehicle",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mileage = forms.IntegerField(
        label="Current Mileage",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
