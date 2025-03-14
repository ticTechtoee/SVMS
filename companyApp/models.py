from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=100, default="KSA")  # Added country field
    city = models.CharField(max_length=100, default="Riyadh")  # Added city field
    address = models.TextField()
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"
