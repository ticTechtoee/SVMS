from django import forms
from .models import (
    Vehicle, VehicleServiceRecord, MaintenanceCategory, MaintenanceTask,
    InspectionItem, SubInspectionItem, ServiceType
)
from companyApp.models import Company
from django.contrib.auth.models import User


# Vehicle Form
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['company', 'user', 'registration_number', 'model', 'manufacturer', 'purchase_date', 'expiry_date', 'is_active']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Registration Number'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Model'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Manufacturer'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class VehicleExpiryUpdateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

# Maintenance Category Form
class MaintenanceCategoryForm(forms.ModelForm):
    class Meta:
        model = MaintenanceCategory
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
        fields = ['name']
        widgets = {
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


# Maintenance Task Form
class MaintenanceTaskForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = ['category', 'main_item', 'sub_item', 'service_type', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'main_item': forms.Select(attrs={'class': 'form-control'}),
            'sub_item': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }

class VehicleMileageForm(forms.Form):
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mileage_at_service = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mileage'})
    )

# # Vehicle Service Record Form
# class VehicleServiceRecordForm(forms.ModelForm):
#     class Meta:
#         model = VehicleServiceRecord
#         fields = ['vehicle', 'mileage_at_service', 'maintenance_category', 'main_item', 'sub_item', 'service_type', 'description']
#         widgets = {
#             'vehicle': forms.Select(attrs={'class': 'form-control'}),
#             'mileage_at_service': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mileage'}),
#             'maintenance_category': forms.Select(attrs={'class': 'form-control'}),
#             'main_item': forms.Select(attrs={'class': 'form-control'}),
#             'sub_item': forms.Select(attrs={'class': 'form-control'}),
#             'service_type': forms.Select(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Service Description'}),
#         }

class VehicleServiceRecordForm(forms.ModelForm):
    class Meta:
        model = VehicleServiceRecord
        fields = ['vehicle', 'mileage_at_service', 'maintenance_category', 'main_item', 'sub_item', 'service_type', 'description']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'mileage_at_service': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'maintenance_category': forms.Select(attrs={'class': 'form-control'}),
            'main_item': forms.Select(attrs={'class': 'form-control'}),
            'sub_item': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Service Description'}),
        }