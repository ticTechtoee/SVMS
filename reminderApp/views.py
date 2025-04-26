from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from vehicleApp.models import Vehicle

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reminder

from accountApp.models import Employee

@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(status='pending')
    return render(request, 'reminderApp/reminder.html', {'reminders': reminders})

@login_required
def mark_reminder_completed(request, reminder_id):
    reminder = Reminder.objects.get(id=reminder_id)
    reminder.status = 'completed'
    reminder.save()
    return redirect('reminderApp:reminder_list')



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



@login_required
def vehicle_expiry_notifications(request):
    today = now().date()
    vehicles = None

    if request.user.is_superuser:
        vehicles = Vehicle.objects.all()
    else:
        company = get_user_company(request.user)
        vehicles = Vehicle.objects.filter(company=company)

    expiring_vehicles = []
    for vehicle in vehicles:
        if vehicle.is_expired() or vehicle.is_near_expiry():
            expiring_vehicles.append({
                'vehicle': vehicle,
                'message': "Vehicle is expired" if vehicle.is_expired() else "Vehicle is near expiry",
                'date': vehicle.expiry_date,
            })

    # 🚀 Pagination
    paginator = Paginator(expiring_vehicles, 10)  # Show 10 vehicles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reminderApp/vehicle_expiry_notifications.html', {
        'page_obj': page_obj,
    })



def notification_list(request):
    reminders = Reminder.objects.filter(is_read=False).order_by('-reminder_date')
    return render(request, "reminderApp/notification_list.html", {"reminders": reminders})
