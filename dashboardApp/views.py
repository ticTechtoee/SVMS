from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from companyApp.models import Company
from vehicleApp.models import Vehicle
from vehicleApp.models import VehicleServiceRecord  # Import maintenance records
from django.shortcuts import render, get_object_or_404
from vehicleApp.models import Vehicle, VehicleServiceRecord
from django.http import HttpResponseForbidden


def is_admin(user):
    return user.is_superuser or user.is_staff


@login_required
def admin_dashboard(request):
    if is_admin(request.user):
        users_count = User.objects.count()
        companies_count = Company.objects.count()
        vehicles = Vehicle.objects.all().order_by('-purchase_date')[:5]
        vehicles_count = Vehicle.objects.count()
        maintenance_count = VehicleServiceRecord.objects.count()
        maintenance_users_count = User.objects.filter(vehicle__vehicleservicerecord__isnull=False).distinct().count()

        users = User.objects.all().order_by('-date_joined')[:5]
        companies = Company.objects.all().order_by('-name')[:5]
    else:
        vehicles = Vehicle.objects.filter(user=request.user).order_by('-purchase_date')[:5]
        users_count = 1
        companies_count = 1 if vehicles.exists() else 0
        vehicles_count = vehicles.count()
        maintenance_count = VehicleServiceRecord.objects.filter(vehicle__user=request.user).count()
        maintenance_users_count = 1 if maintenance_count > 0 else 0

        users = [request.user]
        companies = list(set([v.company for v in vehicles]))

    selected_vehicle = request.GET.get('vehicle_id')
    if selected_vehicle:
        if is_admin(request.user):
            selected_maintenance_count = VehicleServiceRecord.objects.filter(vehicle_id=selected_vehicle).count()
        else:
            selected_maintenance_count = VehicleServiceRecord.objects.filter(
                vehicle_id=selected_vehicle,
                vehicle__user=request.user
            ).count()
    else:
        selected_maintenance_count = None

    context = {
        'users_count': users_count,
        'companies_count': companies_count,
        'vehicles_count': vehicles_count,
        'maintenance_count': maintenance_count,
        'maintenance_users_count': maintenance_users_count,
        'users': users,
        'companies': companies,
        'vehicles': vehicles,
        'selected_maintenance_count': selected_maintenance_count,
        'selected_vehicle': selected_vehicle,
    }

    return render(request, 'dashboardApp/admin_dashboard.html', context)


@login_required
def vehicle_maintenance_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Ensure user can access only their vehicles
    if not is_admin(request.user) and vehicle.user != request.user:
        return HttpResponseForbidden("You do not have permission to view this vehicle's records.")

    maintenance_records = VehicleServiceRecord.objects.filter(vehicle=vehicle).select_related(
        'maintenance_type', 'main_item', 'sub_item', 'service_type', 'vehicle__user'
    )

    context = {
        'vehicle': vehicle,
        'maintenance_records': maintenance_records,
    }
    return render(request, 'dashboardApp/maintenance_detail.html', context)


@login_required
def viewUserDetail(request):
    users = User.objects.all()  # Fetch all registered users
    return render(request, "home/UserDetailView.html", {"users": users})