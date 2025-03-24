from .models import Reminder

def reminder_count(request):
    if request.user.is_authenticated:
        reminders = Reminder.objects.filter(status='pending')
        return {'reminders': reminders, 'reminder_count': reminders.count()}
    return {'reminders': [], 'reminder_count': 0}

