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
        queryset=Vehicle.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'data-placeholder': 'Select or search vehicle...'
        })
    )

    mileage_at_service = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mileage'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        selected_company = kwargs.pop('selected_company', None)
        super().__init__(*args, **kwargs)

        # Superuser logic
        if user and user.is_superuser:
            if not selected_company:
                selected_company = Company.objects.first()
            self.fields['vehicle'].queryset = Vehicle.objects.filter(company=selected_company)
            self.fields['company'].initial = selected_company

        # Employee logic
        else:
            self.fields.pop('company')  # Employees don't need to pick a company
            from accountApp.models import Employee
            try:
                employee = Employee.objects.get(user=user)
                self.fields['vehicle'].queryset = Vehicle.objects.filter(company=employee.company)
            except Employee.DoesNotExist:
                self.fields['vehicle'].queryset = Vehicle.objects.none()






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












#         I used to have a system where I have divided the Vehicle Maintenance Record into 2 steps ```
# @login_required
# def select_vehicle_mileage(request):
#     selected_company = None

#     if request.method == "POST":
#         company_id = request.POST.get('company')

#         if request.user.is_superuser and company_id:
#             selected_company = Company.objects.get(id=company_id)

#         form = VehicleMileageForm(request.POST, user=request.user, selected_company=selected_company)

#         if form.is_valid():
#             vehicle = form.cleaned_data['vehicle']
#             mileage = form.cleaned_data['mileage_at_service']

#             maintenance_category = MaintenanceType.objects.filter(
#                 kilometer__lte=mileage
#             ).order_by('-kilometer').first()

#             return redirect('vehicleApp:create_service_record_step2', vehicle.id, mileage, maintenance_category.id if maintenance_category else 0)

#     else:
#         form = VehicleMileageForm(user=request.user)

#     return render(request, 'vehicleApp/select_vehicle_mileage.html', {'form': form})




# @login_required
# def create_service_record_step2(request, vehicle_id, mileage, category_id):
#     vehicle = Vehicle.objects.get(id=vehicle_id)
#     maintenance_category = MaintenanceType.objects.get(id=category_id) if category_id != 0 else None

#     if request.method == "POST":
#         form = VehicleServiceRecordForm(request.POST)
#         if form.is_valid():
#             service_record = form.save(commit=False)
#             service_record.mechanic = request.user  # Automatically assign the logged-in user
#             service_record.save()
#             return redirect('vehicleApp:service_record_list')  # Redirect to list page

#     else:
#         form = VehicleServiceRecordForm(initial={
#             'vehicle': vehicle,
#             'mileage_at_service': mileage,
#             'maintenance_category': maintenance_category,
#         })

#     return render(request, 'vehicleApp/create_service_record.html', {'form': form})```. 1 Step would let the user select the company (if user is an admin) and select the vehicle then enter the number of kilometers or mileage and enter, here was the magic, the system automatically searches in the ```# Maintenance Type (renamed from Category)
# class MaintenanceType(models.Model):
#     TYPE_CHOICES = [
#         ('A', 'صیانہ و قائیہ'),
#         ('B', 'صیانہ متوسطہ'),
#         ('C', 'صیانہ شاملہ 1'),
#         ('D', 'صیانہ شاملہ 2'),
#     ]
#     name = models.CharField(max_length=1, choices=TYPE_CHOICES)
#     kilometer = models.IntegerField()
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.get_name_display()} ({self.kilometer})"``` model with kilometers (because kilometer value only exist in 1 category) for example if kilometers were 20000 system would search the model 20000 kilometers are liked with `        ('C', 'صیانہ شاملہ 1'),` that's why that was fetch and selects the `maintenance type` in this form ```class VehicleServiceRecordForm(forms.ModelForm):
#     class Meta:
#         model = VehicleServiceRecord
#         fields = ['vehicle', 'mileage_at_service', 'maintenance_type', 'main_item', 'sub_item', 'service_type', 'description']
#         widgets = {
#             'vehicle': forms.Select(attrs={'class': 'form-control'}),
#             'mileage_at_service': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
#             'maintenance_type': forms.Select(attrs={'class': 'form-control'}),
#             'main_item': forms.Select(attrs={'class': 'form-control'}),
#             'sub_item': forms.Select(attrs={'class': 'form-control'}),
#             'service_type': forms.Select(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Service Description'}),
#         }``` this feature is not working now. Can we make it work?