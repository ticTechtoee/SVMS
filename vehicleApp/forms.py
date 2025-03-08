from django import forms
from .models import Vehicle
from .models import MaintenanceRecord, VehicleMaintenanceSchedule

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['company', 'registration_number', 'model', 'manufacturer', 'purchase_date', 'is_active']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Registration Number'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Model'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Manufacturer'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['vehicle', 'service_date', 'cost', 'description']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'service_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class VehicleMaintenanceScheduleForm(forms.ModelForm):
    class Meta:
        model = VehicleMaintenanceSchedule
        fields = ['vehicle', 'interval', 'task', 'scheduled_date', 'status', 'performed_date', 'notes']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'interval': forms.Select(attrs={'class': 'form-control'}),
            'task': forms.Select(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'performed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
