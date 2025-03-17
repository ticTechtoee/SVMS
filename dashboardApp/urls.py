from django.urls import path
from .views import admin_dashboard, vehicle_maintenance_detail

app_name = 'dashboardApp'

urlpatterns = [
    path('detail/', admin_dashboard, name='admin_dashboard'),
    path('vehicle/<str:vehicle_id>/maintenance/', vehicle_maintenance_detail, name='vehicle_maintenance_detail'),
]
