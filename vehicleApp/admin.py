from django.contrib import admin
from .models import Vehicle, MaintenanceInterval, MaintenanceTask, MaintenanceRecord, VehicleMaintenanceSchedule

admin.site.register(Vehicle)
admin.site.register(MaintenanceInterval)
admin.site.register(MaintenanceTask)
admin.site.register(MaintenanceRecord)
admin.site.register(VehicleMaintenanceSchedule)