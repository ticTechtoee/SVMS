from django import forms
from vehicleApp.models import Vehicle

class PredictionForm(forms.Form):
    vehicle_id = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        label="Select Vehicle",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="-- Select Vehicle --"
    )

    mileage = forms.IntegerField(
        label="Current Mileage",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)
        self.fields['vehicle_id'].label_from_instance = lambda obj: f"{obj.registration_number} ({obj.model})"
