from django.urls import path
from .views import reminder_list, mark_reminder_completed

app_name = 'reminderApp'

urlpatterns = [
    path('list/', reminder_list, name='reminder_list'),
    path('mark_completed/<int:reminder_id>/', mark_reminder_completed, name='mark_reminder_completed'),
]
