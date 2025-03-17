from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from companyApp.models import Company
from vehicleApp.models import Vehicle
from vehicleApp.models import VehicleServiceRecord  # Import maintenance records

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:  # Ensure only admin can access
        return render(request, '403.html', status=403)

    users_count = User.objects.count()
    companies_count = Company.objects.count()
    vehicles_count = Vehicle.objects.count()
    maintenance_count = VehicleServiceRecord.objects.count()
    maintenance_users_count = User.objects.filter(vehicle__vehicleservicerecord__isnull=False).distinct().count()


    users = User.objects.all().order_by('-date_joined')[:5]
    companies = Company.objects.all().order_by('-created_at')[:5]
    vehicles = Vehicle.objects.all().order_by('-created_at')[:5]

    selected_vehicle = request.GET.get('vehicle_id')  # Get vehicle from dropdown
    if selected_vehicle:
        selected_maintenance_count = VehicleServiceRecord.objects.filter(vehicle_id=selected_vehicle).count()
    else:
        selected_maintenance_count = None  # Default when no vehicle selected

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
