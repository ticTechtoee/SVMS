from django.db import models
from companyApp.models import Company
from django.contrib.auth.models import User


# Vehicle App
class Vehicle(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    purchase_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.registration_number

# Maintenance App
class MaintenanceInterval(models.Model):
    name = models.CharField(max_length=50, unique=True)
    interval_km = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MaintenanceTask(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    default_duration = models.IntegerField(null=True, blank=True)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance Record for {self.vehicle}"

class VehicleMaintenanceSchedule(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    STATUS_CHOICES = [(PENDING, 'Pending'), (COMPLETED, 'Completed')]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    interval = models.ForeignKey(MaintenanceInterval, on_delete=models.CASCADE)
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    performed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.vehicle} - {self.task} ({self.status})"


