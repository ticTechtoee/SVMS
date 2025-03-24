from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reminder

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

def vehicle_expiry_notifications(request):
    reminders = Reminder.objects.filter(status=Reminder.PENDING).order_by('-created_at')
    return render(request, 'reminderApp/vehicle_expiry_notifications.html', {'reminders': reminders})


def notification_list(request):
    reminders = Reminder.objects.filter(is_read=False).order_by('-created_at')
    return render(request, "reminderApp/notification_list.html", {"reminders": reminders})
