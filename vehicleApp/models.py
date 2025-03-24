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
    is_active = models.BooleanField(default=True)
    near_expiry_notified = models.BooleanField(default=False)  # ✅ New Field to Track Notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_near_expiry(self):
        """Check if the vehicle is within 15 days of expiry."""
        return self.expiry_date - timedelta(days=15) <= now().date() <= self.expiry_date

    def is_expired(self):
        """Check if the vehicle is expired."""
        return self.expiry_date < now().date()

    def __str__(self):
        return self.registration_number


# Maintenance Categories
class MaintenanceCategory(models.Model):
    CATEGORY_CHOICES = [
        ('A', 'صیانہ و قائیہ'),
        ('B', 'صیانہ متوسطہ'),
        ('C', 'صیانہ شاملہ 1'),
        ('D', 'صیانہ شاملہ 2'),
    ]
    name = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    kilometer = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_name_display()} ({self.kilometer})"


# Main Inspection Items (e.g., Engine, Power Train, Brakes, etc.)
class InspectionItem(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Example: Engine, Power Train

    def __str__(self):
        return self.name


# Sub-Items under each Main Inspection Item
class SubInspectionItem(models.Model):
    main_item = models.ForeignKey(
        InspectionItem, on_delete=models.CASCADE, related_name="sub_items"
    )
    name = models.CharField(max_length=50)  # Example: Engine Oil, Air Filter, Clutch Mechanics

    def __str__(self):
        return f"{self.name} ({self.main_item.name})"


# Service Types (Replace, Inspect, Adjust, etc.)
class ServiceType(models.Model):
    SERVICE_CHOICES = [
        ('R', 'Replace'),
        ('I', 'Inspect'),
        ('A', 'Adjust'),
        ('C', 'Clean'),
        ('T', 'Test'),
        ('L', 'Lubricate'),
    ]
    code = models.CharField(max_length=1, choices=SERVICE_CHOICES, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.get_code_display()


# Maintenance Task (Links category, items, sub-items, and service type)
class MaintenanceTask(models.Model):
    category = models.ForeignKey(
        MaintenanceCategory, on_delete=models.CASCADE, related_name='maintenance_tasks'
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
        return f"{self.category} - {self.main_item} - {self.sub_item} ({self.service_type})"


class VehicleServiceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    mileage_at_service = models.IntegerField()
    maintenance_category = models.ForeignKey(
        MaintenanceCategory, on_delete=models.CASCADE, related_name="service_records"
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
    mechanic = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.mileage_at_service} km - {self.mechanic.username if self.mechanic else 'Unknown'}"
