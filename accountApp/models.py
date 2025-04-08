from django.db import models
from django.contrib.auth.models import User
from companyApp.models import Company

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[("admin", "Admin"), ("employee", "Employee")])

    def __str__(self):
        return f"{self.user.username} - {self.user.email}"


