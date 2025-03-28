from django.urls import path
from .views import (
    create_vehicle,
    #create_service_record,
    create_maintenance_category,
    create_maintenance_task,
    service_record_list,
    maintenance_category_list,
    maintenance_task_list,
    select_vehicle_mileage,
    create_service_record_step2,
    generate_vehicle_qr,
    vehicle_list,
    update_vehicle_expiry
)

app_name = 'vehicleApp'

urlpatterns = [
    path('create/', create_vehicle, name='create_vehicle'),
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicle/<int:vehicle_id>/update-expiry/', update_vehicle_expiry, name='update_vehicle_expiry'),
    #path('service_record/create/', create_service_record, name='create_service_record'),
    path('select-vehicle/', select_vehicle_mileage, name='select_vehicle_mileage'),
    path('create-service-record/<int:vehicle_id>/<int:mileage>/<int:category_id>/', create_service_record_step2, name='create_service_record_step2'),
    #path('generate-barcode/<int:vehicle_id>/', generate_vehicle_barcode, name='generate_vehicle_barcode'),
    path('generate-qr/<int:vehicle_id>/', generate_vehicle_qr, name='generate_vehicle_qr'),
    path('maintenance/category/create/', create_maintenance_category, name='create_maintenance_category'),
    path('maintenance/task/create/', create_maintenance_task, name='create_maintenance_task'),
    path('service_record/list/', service_record_list, name='service_record_list'),
    path('maintenance/category/list/', maintenance_category_list, name='maintenance_category_list'),
    path('maintenance/task/list/', maintenance_task_list, name='maintenance_task_list'),
]
