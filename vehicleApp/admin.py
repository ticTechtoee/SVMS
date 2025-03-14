from django.contrib import admin
from .models import Vehicle, MaintenanceCategory, InspectionItem, SubInspectionItem, ServiceType, MaintenanceTask, VehicleServiceRecord

admin.site.register(Vehicle)
admin.site.register(MaintenanceCategory)
admin.site.register(InspectionItem)
admin.site.register(SubInspectionItem)
admin.site.register(ServiceType)
admin.site.register(MaintenanceTask)
admin.site.register(VehicleServiceRecord)