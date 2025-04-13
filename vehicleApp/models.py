from django.db import models
from companyApp.models import Company
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

class Vehicle(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    near_expiry_notified = models.BooleanField(default=False)

    def is_near_expiry(self):
        return self.expiry_date - timedelta(days=15) <= now().date() <= self.expiry_date

    def is_expired(self):
        return self.expiry_date < now().date()

    def __str__(self):
        return self.registration_number


# Maintenance Type (renamed from Category)
class MaintenanceType(models.Model):
    TYPE_CHOICES = [
        ('A', 'صیانہ و قائیہ'),
        ('B', 'صیانہ متوسطہ'),
        ('C', 'صیانہ شاملہ 1'),
        ('D', 'صیانہ شاملہ 2'),
    ]
    name = models.CharField(max_length=1, choices=TYPE_CHOICES)
    kilometer = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_name_display()} ({self.kilometer})"


# Main Inspection Items
class InspectionItem(models.Model):
    maintenance_type = models.ForeignKey('MaintenanceType', on_delete=models.CASCADE, related_name="inspection_items")
    name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.name} ({self.maintenance_type.get_name_display()})"



# Sub-Items under each Main Inspection Item
class SubInspectionItem(models.Model):
    main_item = models.ForeignKey(
        InspectionItem, on_delete=models.CASCADE, related_name="sub_items"
    )
    name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.name} ({self.main_item.name})"


# Service Types
class ServiceType(models.Model):
    SERVICE_CHOICES = [
        ('R', 'Replace'),
        ('I', 'Inspect'),
        ('A', 'Adjust'),
        ('C', 'Clean'),
        ('T', 'Tight'),
        ('L', 'Lubricate'),
    ]
    code = models.CharField(max_length=1, choices=SERVICE_CHOICES, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.get_code_display()


# Maintenance Task
class MaintenanceTask(models.Model):
    maintenance_type = models.ForeignKey(
        MaintenanceType, on_delete=models.CASCADE, related_name='maintenance_tasks'
    )
    main_item = models.ForeignKey(
        InspectionItem, on_delete=models.CASCADE, related_name='maintenance_tasks'
    )
    sub_item = models.ForeignKey(
        SubInspectionItem, on_delete=models.CASCADE, related_name='maintenance_tasks'
    )
    service_type = models.ForeignKey(
        ServiceType, on_delete=models.CASCADE, related_name='maintenance_tasks'
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.maintenance_type} - {self.main_item} - {self.sub_item} ({self.service_type})"


class VehicleServiceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    mileage_at_service = models.IntegerField()
    maintenance_type = models.ForeignKey(
        MaintenanceType, on_delete=models.CASCADE, related_name="service_records"
    )
    main_item = models.ForeignKey(
        InspectionItem, on_delete=models.CASCADE, related_name="service_records"
    )
    sub_item = models.ForeignKey(
        SubInspectionItem, on_delete=models.CASCADE, related_name="service_records"
    )
    service_type = models.ForeignKey(
        ServiceType, on_delete=models.CASCADE, related_name="service_records"
    )
    description = models.TextField(blank=True, null=True)
    mechanic = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.mileage_at_service} km - {self.mechanic.username if self.mechanic else 'Unknown'}"



