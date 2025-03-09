from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import VehicleForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import MaintenanceRecord, VehicleMaintenanceSchedule
from .forms import MaintenanceRecordForm, VehicleMaintenanceScheduleForm

@login_required
def create_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            return redirect('dashboardApp:admin_dashboard')
    else:
        form = VehicleForm()

    return render(request, 'vehicleApp/create_vehicle.html', {'form': form})



@login_required
def create_maintenance_record(request):
    if request.method == "POST":
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicleApp:maintenance_list')  # Redirect to maintenance list
    else:
        form = MaintenanceRecordForm()

    return render(request, 'vehicleApp/create_maintenance_record.html', {'form': form})

@login_required
def create_maintenance_schedule(request):
    if request.method == "POST":
        form = VehicleMaintenanceScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicleApp:maintenance_schedule_list')  # Redirect to schedule list
    else:
        form = VehicleMaintenanceScheduleForm()

    return render(request, 'vehicleApp/create_maintenance_schedule.html', {'form': form})

@login_required
def maintenance_list(request):
    records = MaintenanceRecord.objects.all().order_by('-service_date')
    return render(request, 'vehicleApp/maintenance_list.html', {'records': records})

@login_required
def maintenance_schedule_list(request):
    schedules = VehicleMaintenanceSchedule.objects.all().order_by('-scheduled_date')
    return render(request, 'vehicleApp/maintenance_schedule_list.html', {'schedules': schedules})
