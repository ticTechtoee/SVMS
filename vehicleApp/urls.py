from django.urls import path
from .views import (
    create_vehicle,
    create_inspection_item,
    create_sub_inspection_item,
    create_service_type,
    service_record_list,
    create_maintenance_type,
    maintenance_category_list,
    select_vehicle_mileage,
    create_service_record_step2,
    generate_vehicle_qr,
    vehicle_list,
    update_vehicle_expiry,
    delete_vehicle,
    maintenance_type_report,
    get_vehicles_by_company,
    combined_maintenance_report,
    emergency_maintenance_create,
    emergency_maintenance_list
)

app_name = 'vehicleApp'

urlpatterns = [
    path('create/', create_vehicle, name='create_vehicle'),
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('ajax/get-vehicles/', get_vehicles_by_company, name='ajax_get_vehicles'),
    path('combined-maintenance-report/', combined_maintenance_report, name='combined_maintenance_report'),
    path('vehicle/<int:vehicle_id>/update-expiry/', update_vehicle_expiry, name='update_vehicle_expiry'),
    path('vehicle/<int:vehicle_id>/delete-vehilce/', delete_vehicle, name='delete_vehicle'),
    path('select-vehicle/', select_vehicle_mileage, name='select_vehicle_mileage'),
    path('create-service-record/<int:vehicle_id>/<int:mileage>/<int:category_id>/', create_service_record_step2, name='create_service_record_step2'),
    path('generate-qr/<int:vehicle_id>/', generate_vehicle_qr, name='generate_vehicle_qr'),

    # Maintenance Forms
    path('maintenance/category/create/', create_maintenance_type, name='create_maintenance_category'),
    path('maintenance/inspection-item/create/', create_inspection_item, name='create_inspection_item'),
    path('maintenance/sub-inspection-item/create/', create_sub_inspection_item, name='create_sub_inspection_item'),
    path('maintenance/service-type/create/', create_service_type, name='create_service_type'),

    # Lists
    path('service_record/list/', service_record_list, name='service_record_list'),
    path('maintenance/category/list/', maintenance_category_list, name='maintenance_category_list'),

    path('maintenance/report/', maintenance_type_report, name='maintenance_type_report'),
    path('maintenance/emergency-record/', emergency_maintenance_create, name='emergency_maintenance_create'),
    path('maintenance/emergency-vehicle-list/', emergency_maintenance_list, name='emergency_maintenance_list'),


]
