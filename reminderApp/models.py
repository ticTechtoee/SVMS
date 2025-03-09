from django.db import models
from vehicleApp.models import Vehicle
# Create your models here.
# Reminder App
class Reminder(models.Model):
    SERVICE = 'service'
    INSURANCE = 'insurance'
    EMISSION = 'emission'
    TYPE_CHOICES = [(SERVICE, 'Service'), (INSURANCE, 'Insurance'), (EMISSION, 'Emission')]

    PENDING = 'pending'
    COMPLETED = 'completed'
    STATUS_CHOICES = [(PENDING, 'Pending'), (COMPLETED, 'Completed')]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    reminder_date = models.DateField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle} - {self.type} ({self.status})"