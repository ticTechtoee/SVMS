from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from companyApp.models import Company
from vehicleApp.models import Vehicle

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:  # Ensure only admin can access
        return render(request, '403.html', status=403)

    users_count = User.objects.count()
    companies_count = Company.objects.count()
    vehicles_count = Vehicle.objects.count()

    users = User.objects.all().order_by('-date_joined')[:5]  # Show latest 5 users
    companies = Company.objects.all().order_by('-created_at')[:5]  # Latest companies
    vehicles = Vehicle.objects.all().order_by('-created_at')[:5]  # Latest vehicles

    context = {
        'users_count': users_count,
        'companies_count': companies_count,
        'vehicles_count': vehicles_count,
        'users': users,
        'companies': companies,
        'vehicles': vehicles,
    }

    return render(request, 'dashboardApp/admin_dashboard.html', context)

