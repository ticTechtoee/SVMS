from django import forms
from .models import (
    Vehicle, VehicleServiceRecord, MaintenanceType,
    InspectionItem, SubInspectionItem, ServiceType
)
from companyApp.models import Company
from django.contrib.auth.models import User

from django import forms
from .models import MaintenanceType, InspectionItem, SubInspectionItem, ServiceType, Vehicle, VehicleServiceRecord
# forms.py

from companyApp.models import Company
# vehicleApp/forms.py

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['company', 'user']  # Exclude these from the form
        widgets = {
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Registration Number'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Model'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Manufacturer'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class VehicleExpiryUpdateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }


# Maintenance Type Form
class MaintenanceTypeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceType
        fields = ['name', 'kilometer', 'description']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'kilometer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Kilometer'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }

# Inspection Item Form
class InspectionItemForm(forms.ModelForm):
    class Meta:
        model = InspectionItem
        fields = ['maintenance_type', 'name']
        widgets = {
            'maintenance_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Inspection Item Name'}),
        }

# Sub-Inspection Item Form
class SubInspectionItemForm(forms.ModelForm):
    class Meta:
        model = SubInspectionItem
        fields = ['main_item', 'name']
        widgets = {
            'main_item': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sub-Inspection Item Name'}),
        }


# Service Type Form
class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ['code', 'description']
        widgets = {
            'code': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Service Description'}),
        }




class VehicleMileageForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.none(),  # Initially empty
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    mileage_at_service = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mileage'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        selected_company = kwargs.pop('selected_company', None)
        super().__init__(*args, **kwargs)

        # Show company dropdown only for superusers
        if not user.is_superuser:
            self.fields.pop('company')
            from accountApp.models import Employee
            try:
                employee = Employee.objects.get(user=user)
                self.fields['vehicle'].queryset = Vehicle.objects.filter(company=employee.company)
            except Employee.DoesNotExist:
                self.fields['vehicle'].queryset = Vehicle.objects.none()
        else:
            if selected_company:
                self.fields['vehicle'].queryset = Vehicle.objects.filter(company=selected_company)



class VehicleServiceRecordForm(forms.ModelForm):
    class Meta:
        model = VehicleServiceRecord
        fields = ['vehicle', 'mileage_at_service', 'maintenance_type', 'main_item', 'sub_item', 'service_type', 'description']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'mileage_at_service': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'maintenance_type': forms.Select(attrs={'class': 'form-control'}),
            'main_item': forms.Select(attrs={'class': 'form-control'}),
            'sub_item': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Service Description'}),
        }