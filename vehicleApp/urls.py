from django.urls import path
from .views import create_vehicle

from django.urls import path
from .views import create_maintenance_record, create_maintenance_schedule, maintenance_list, maintenance_schedule_list


app_name = 'vehicleApp'

urlpatterns = [
    path('create/', create_vehicle, name='create_vehicle'),
    path('maintenance/create/', create_maintenance_record, name='create_maintenance_record'),
    path('maintenance/schedule/create/', create_maintenance_schedule, name='create_maintenance_schedule'),
    path('maintenance/list/', maintenance_list, name='maintenance_list'),
    path('maintenance/schedule/list/', maintenance_schedule_list, name='maintenance_schedule_list'),
]
