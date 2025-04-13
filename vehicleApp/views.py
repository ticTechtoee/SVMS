from .models import Vehicle, MaintenanceType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Vehicle, VehicleServiceRecord, MaintenanceType, MaintenanceTask
from .forms import VehicleForm, VehicleServiceRecordForm, VehicleMileageForm, VehicleExpiryUpdateForm
import io


from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import VehicleServiceRecord, Vehicle

import qrcode
import io
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VehicleServiceRecord, Vehicle
from accountApp.models import Employee


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MaintenanceTypeForm, InspectionItemForm, SubInspectionItemForm, ServiceTypeForm
from .models import MaintenanceType, InspectionItem, SubInspectionItem, ServiceType


@login_required
def create_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user

            try:
                employee = Employee.objects.get(user=request.user)
                vehicle.company = employee.company
            except Employee.DoesNotExist:
                # fallback for superuser or error
                return redirect('home:HomeView')  # or show an error message

            vehicle.save()
            return redirect('vehicleApp:vehicle_list')
    else:
        form = VehicleForm()

    return render(request, 'vehicleApp/create_vehicle.html', {'form': form})

# WVAm6tS8wV

@login_required
def vehicle_list(request):
    if request.user.is_superuser:
        vehicles = Vehicle.objects.all()
        print("User is Admin")
    else:
        # Get the company of the logged-in user
        try:
            employee = Employee.objects.get(user=request.user)
            vehicles = Vehicle.objects.filter(company=employee.company)
        except Employee.DoesNotExist:
            return redirect('home:HomeView')

    return render(request, 'vehicleApp/vehicle_list.html', {'vehicles': vehicles})





@login_required
def update_vehicle_expiry(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        form = VehicleExpiryUpdateForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicleApp:vehicle_list')  # Redirect back to the list

    else:
        form = VehicleExpiryUpdateForm(instance=vehicle)

    return render(request, 'vehicleApp/update_vehicle_expiry.html', {'form': form, 'vehicle': vehicle})




@login_required
def select_vehicle_mileage(request):
    if request.method == "POST":
        form = VehicleMileageForm(request.POST)
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle']
            mileage = form.cleaned_data['mileage_at_service']

            # Find the closest matching maintenance category based on mileage
            maintenance_category = MaintenanceType.objects.filter(
                kilometer__lte=mileage
            ).order_by('-kilometer').first()  # Get the closest lower or equal match

            return redirect('vehicleApp:create_service_record_step2', vehicle.id, mileage, maintenance_category.id if maintenance_category else 0)

    else:
        form = VehicleMileageForm()

    return render(request, 'vehicleApp/select_vehicle_mileage.html', {'form': form})


@login_required
def create_service_record_step2(request, vehicle_id, mileage, category_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    maintenance_category = MaintenanceType.objects.get(id=category_id) if category_id != 0 else None

    if request.method == "POST":
        form = VehicleServiceRecordForm(request.POST)
        if form.is_valid():
            service_record = form.save(commit=False)
            service_record.mechanic = request.user  # Automatically assign the logged-in user
            service_record.save()
            return redirect('vehicleApp:service_record_list')  # Redirect to list page

    else:
        form = VehicleServiceRecordForm(initial={
            'vehicle': vehicle,
            'mileage_at_service': mileage,
            'maintenance_category': maintenance_category,
        })

    return render(request, 'vehicleApp/create_service_record.html', {'form': form})






# @login_required
# def create_maintenance_task(request):
#     if request.method == "POST":
#         form = MaintenanceTaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('vehicleApp:maintenance_task_list')  # Redirect to task list
#     else:
#         form = MaintenanceTaskForm()

#     return render(request, 'vehicleApp/create_maintenance_task.html', {'form': form})


@login_required
def service_record_list(request):
    vehicles = Vehicle.objects.all()
    selected_vehicle_id = request.GET.get('vehicle', None)

    records = VehicleServiceRecord.objects.filter(vehicle_id=selected_vehicle_id) if selected_vehicle_id else VehicleServiceRecord.objects.all()

    return render(request, 'vehicleApp/service_record_list.html', {
        'records': records,
        'vehicles': vehicles,
        'selected_vehicle_id': selected_vehicle_id
    })


@login_required
def generate_vehicle_qr(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    service_records = VehicleServiceRecord.objects.filter(vehicle=vehicle)

    # Prepare QR code data (vehicle details + service history)
    qr_data = f"Vehicle: {vehicle.registration_number}\n"
    for record in service_records:
        qr_data += f"{record.mileage_at_service} km - {record.maintenance_category}\n"

    # Generate QR Code
    qr = qrcode.make(qr_data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")

    return HttpResponse(buffer.getvalue(), content_type="image/png")


@login_required
def maintenance_category_list(request):
    categories = MaintenanceType.objects.all()
    return render(request, 'vehicleApp/maintenance_category_list.html', {'categories': categories})


# @login_required
# def maintenance_task_list(request):
#     tasks = MaintenanceTask.objects.all().order_by('category')
#     return render(request, 'vehicleApp/maintenance_task_list.html', {'tasks': tasks})



# Create Maintenance Type View
@login_required
def create_maintenance_type(request):
    if request.method == "POST":
        form = MaintenanceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicleApp:maintenance_category_list')  # Redirect to type list
    else:
        form = MaintenanceTypeForm()

    return render(request, 'vehicleApp/create_maintenance_category.html', {'form': form})

# Create Inspection Item View
@login_required
def create_inspection_item(request):
    if request.method == "POST":
        form = InspectionItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboardApp:admin_dashboard')  # Redirect to inspection item list
    else:
        form = InspectionItemForm()

    return render(request, 'vehicleApp/create_inspection_item.html', {'form': form})

# Create Sub-Inspection Item View
@login_required
def create_sub_inspection_item(request):
    if request.method == "POST":
        form = SubInspectionItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboardApp:admin_dashboard') # Redirect to sub-inspection item list
    else:
        form = SubInspectionItemForm()

    return render(request, 'vehicleApp/create_sub_inspection_item.html', {'form': form})

# Create Service Type View
@login_required
def create_service_type(request):
    if request.method == "POST":
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboardApp:admin_dashboard')  # Redirect to service type list
    else:
        form = ServiceTypeForm()

    return render(request, 'vehicleApp/create_service_type.html', {'form': form})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import MaintenanceType, VehicleServiceRecord
import openpyxl
from django.http import HttpResponse

@login_required

def maintenance_type_report(request):
    selected_type_id = request.GET.get('maintenance_type')
    maintenance_types = MaintenanceType.objects.all()
    records = []

    if selected_type_id:
        maintenance_type = MaintenanceType.objects.get(id=selected_type_id)
        records = VehicleServiceRecord.objects.filter(
            maintenance_type=maintenance_type
        ).select_related('vehicle__company', 'vehicle__user', 'maintenance_type')

        # If exporting to Excel
        if 'export' in request.GET:
            return export_to_excel(records, maintenance_type)

    return render(request, 'vehicleApp/maintenance_type_report.html', {
        'maintenance_types': maintenance_types,
        'records': records,
        'selected_type_id': int(selected_type_id) if selected_type_id else None
    })



def export_to_excel(records, maintenance_type):
    from django.utils.text import slugify

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Maintenance Report"

    # Header row
    ws.append([
        "Vehicle", "Created By", "Company", "Mileage",
        "Main Item", "Sub Item", "Service Type", "Mechanic"
    ])

    for record in records:
        ws.append([
            record.vehicle.registration_number,
            record.vehicle.user.username,
            record.vehicle.company.name,
            f"{record.mileage_at_service} km",
            record.main_item.name,
            record.sub_item.name,
            record.service_type.get_code_display(),
            record.mechanic.username if record.mechanic else 'N/A'
        ])

    # Use the display name for the filename
    filename = f"{slugify(maintenance_type.get_name_display())}_report.xlsx"

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response

