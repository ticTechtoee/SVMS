from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Vehicle, VehicleServiceRecord, MaintenanceCategory, MaintenanceTask
from .forms import VehicleForm, VehicleServiceRecordForm, MaintenanceCategoryForm, MaintenanceTaskForm, VehicleMileageForm
import io
import barcode
from barcode.writer import ImageWriter
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import VehicleServiceRecord, Vehicle


@login_required
def create_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            return redirect('dashboardApp:admin_dashboard')  # Redirect to the admin dashboard
    else:
        form = VehicleForm()

    return render(request, 'vehicleApp/create_vehicle.html', {'form': form})

@login_required
def select_vehicle_mileage(request):
    if request.method == "POST":
        form = VehicleMileageForm(request.POST)
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle']
            mileage = form.cleaned_data['mileage_at_service']

            # Find the closest matching maintenance category based on mileage
            maintenance_category = MaintenanceCategory.objects.filter(
                kilometer__lte=mileage
            ).order_by('-kilometer').first()  # Get the closest lower or equal match

            return redirect('vehicleApp:create_service_record_step2', vehicle.id, mileage, maintenance_category.id if maintenance_category else 0)

    else:
        form = VehicleMileageForm()

    return render(request, 'vehicleApp/select_vehicle_mileage.html', {'form': form})

# @login_required
# def create_service_record(request):
#     if request.method == "POST":
#         form = VehicleServiceRecordForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('vehicleApp:service_record_list')  # Redirect to service record list
#     else:
#         form = VehicleServiceRecordForm()

#     return render(request, 'vehicleApp/create_service_record.html', {'form': form})

@login_required
def create_service_record_step2(request, vehicle_id, mileage, category_id):
    from .models import Vehicle, MaintenanceCategory

    vehicle = Vehicle.objects.get(id=vehicle_id)
    maintenance_category = MaintenanceCategory.objects.get(id=category_id) if category_id != 0 else None

    if request.method == "POST":
        form = VehicleServiceRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicleApp:service_record_list')  # Redirect to list page

    else:
        form = VehicleServiceRecordForm(initial={
            'vehicle': vehicle,
            'mileage_at_service': mileage,
            'maintenance_category': maintenance_category,
        })

    return render(request, 'vehicleApp/create_service_record.html', {'form': form})


@login_required
def create_maintenance_category(request):
    if request.method == "POST":
        form = MaintenanceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicleApp:maintenance_category_list')  # Redirect to category list
    else:
        form = MaintenanceCategoryForm()

    return render(request, 'vehicleApp/create_maintenance_category.html', {'form': form})


@login_required
def create_maintenance_task(request):
    if request.method == "POST":
        form = MaintenanceTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicleApp:maintenance_task_list')  # Redirect to task list
    else:
        form = MaintenanceTaskForm()

    return render(request, 'vehicleApp/create_maintenance_task.html', {'form': form})


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
def generate_vehicle_barcode(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        service_records = VehicleServiceRecord.objects.filter(vehicle=vehicle)

        # Prepare barcode data (vehicle registration + service history)
        service_data = f"Vehicle: {vehicle.registration_number}\n"
        for record in service_records:
            service_data += f"{record.mileage_at_service} km - {record.maintenance_category}\n"

        # Generate barcode (EAN13 requires a 12-digit number, so we use a hash)
        barcode_data = str(abs(hash(service_data)) % (10**12))  # Generate 12-digit unique hash
        barcode_class = barcode.get_barcode_class('ean13')
        barcode_image = barcode_class(barcode_data, writer=ImageWriter())

        buffer = io.BytesIO()
        barcode_image.write(buffer)

        return HttpResponse(buffer.getvalue(), content_type="image/png")
    except Vehicle.DoesNotExist:
        return HttpResponse("Vehicle not found", status=404)



@login_required
def maintenance_category_list(request):
    categories = MaintenanceCategory.objects.all()
    return render(request, 'vehicleApp/maintenance_category_list.html', {'categories': categories})


@login_required
def maintenance_task_list(request):
    tasks = MaintenanceTask.objects.all().order_by('category')
    return render(request, 'vehicleApp/maintenance_task_list.html', {'tasks': tasks})
