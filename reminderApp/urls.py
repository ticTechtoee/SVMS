from django.urls import path
from .views import reminder_list, mark_reminder_completed, vehicle_expiry_notifications

app_name = 'reminderApp'

urlpatterns = [
    path('list/', reminder_list, name='reminder_list'),
    path('notifications/', vehicle_expiry_notifications, name='vehicle_expiry_notifications'),
    path('mark_completed/<int:reminder_id>/', mark_reminder_completed, name='mark_reminder_completed'),
]
