from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['company', 'user', 'registration_number', 'model', 'manufacturer', 'purchase_date', 'is_active']
