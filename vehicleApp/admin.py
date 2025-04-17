from django.contrib import admin
from .models import Vehicle, MaintenanceType, InspectionItem, SubInspectionItem, ServiceType, VehicleServiceRecord

admin.site.register(Vehicle)
admin.site.register(MaintenanceType)
admin.site.register(InspectionItem)
admin.site.register(SubInspectionItem)
admin.site.register(ServiceType)

admin.site.register(VehicleServiceRecord)