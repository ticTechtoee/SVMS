from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accountApp.models import Employee
from companyApp.models import Company
from vehicleApp.models import Vehicle
from vehicleApp.models import VehicleServiceRecord
from django.shortcuts import render, get_object_or_404
from vehicleApp.models import Vehicle, VehicleServiceRecord
from django.http import HttpResponseForbidden






def get_user_company(user):
    """
    Returns the Company instance associated with the given user via Employee model.
    Returns None if the user is not linked to any company.
    """
    try:
        employee = Employee.objects.get(user=user)
        return employee.company
    except Employee.DoesNotExist:
        return None




def is_admin(user):
    return user.is_superuser or user.is_staff

def is_company_admin(user):
    try:
        print(user.employee.role)
        return user.employee.role == "company_admin"

    except Employee.DoesNotExist:
        return False

def is_employee(user):
    try:
        return user.employee.role == "employee"
    except Employee.DoesNotExist:
        return False


@login_required
def admin_dashboard(request):
    user = request.user

    # Determine user role
    if is_admin(user):
        role = "Admin"
        company = None
    elif is_company_admin(user):
        role = "Company Admin"
        company = get_user_company(user)
        if not company:
            return render(request, 'dashboardApp/no_company.html')
    elif is_employee(user):
        role = "Employee"
        company = get_user_company(user)
    else:
        role = "Unknown"
        return render(request, 'dashboardApp/unauthorized.html')

    # Data fetching based on role
    if role == "Admin":
        users_count = User.objects.count()
        companies_count = Company.objects.count()
        vehicles_for_dropdown = Vehicle.objects.all()
        recent_vehicles = vehicles_for_dropdown.order_by('-purchase_date')[:5]
        vehicles_count = vehicles_for_dropdown.count()
        maintenance_count = VehicleServiceRecord.objects.count()
        maintenance_users_count = User.objects.filter(vehicle__vehicleservicerecord__isnull=False).distinct().count()

        users = User.objects.all().order_by('-date_joined')[:5]
        companies = Company.objects.all().order_by('-name')[:5]

    elif role == "Company Admin":
        vehicles_for_dropdown = Vehicle.objects.filter(company=company)
        recent_vehicles = vehicles_for_dropdown.order_by('-purchase_date')[:5]
        vehicles_count = vehicles_for_dropdown.count()

        users = User.objects.filter(employee__company=company).order_by('-date_joined')[:5]
        users_count = users.count()
        companies_count = 1 if company else 0
        maintenance_count = VehicleServiceRecord.objects.filter(vehicle__company=company).count()
        maintenance_users_count = User.objects.filter(
            vehicle__company=company,
            vehicle__vehicleservicerecord__isnull=False
        ).distinct().count()

        companies = [company]

    elif role == "Employee":
        vehicles_for_dropdown = Vehicle.objects.filter(company=company)
        recent_vehicles = vehicles_for_dropdown.order_by('-purchase_date')[:5]
        vehicles_count = vehicles_for_dropdown.count()

        users = User.objects.filter(employee__company=company).order_by('-date_joined')[:5]
        users_count = users.count()
        companies_count = 1 if company else 0
        maintenance_count = VehicleServiceRecord.objects.filter(vehicle__company=company).count()
        maintenance_users_count = User.objects.filter(
            vehicle__company=company,
            vehicle__vehicleservicerecord__isnull=False
        ).distinct().count()

        companies = [company]


    # Optional vehicle-specific maintenance filter
    selected_vehicle = request.GET.get('vehicle_id')
    selected_maintenance_count = None

    if selected_vehicle:
        qs = VehicleServiceRecord.objects.filter(vehicle_id=selected_vehicle)
        if company:
            qs = qs.filter(vehicle__company=company)
        selected_maintenance_count = qs.count()

    context = {
        'role': role,
        'company': company,
        'users_count': users_count,
        'companies_count': companies_count,
        'vehicles_count': vehicles_count,
        'maintenance_count': maintenance_count,
        'maintenance_users_count': maintenance_users_count,
        'users': users,
        'companies': companies,
        'vehicles': recent_vehicles,
        'vehicles_for_dropdown': vehicles_for_dropdown,
        'selected_maintenance_count': selected_maintenance_count,
        'selected_vehicle': selected_vehicle,
        'user_role': role,  # Optional: For template logic
    }

    return render(request, 'dashboardApp/admin_dashboard.html', context)





@login_required
def vehicle_maintenance_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Ensure user can access only their vehicles
    if not is_admin(request.user) and not is_company_admin(request.user):
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
    return render(request, "dashboardApp/UserDetailView.html", {"users": users})