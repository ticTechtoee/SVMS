from django.core.management.base import BaseCommand
from vehicleApp.models import Vehicle
from reminderApp.models import Reminder
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "Check for vehicle expiry and create reminders"

    def handle(self, *args, **kwargs):
        today = now().date()
        near_expiry_threshold = today + timedelta(days=15)

        vehicles = Vehicle.objects.filter(is_active=True)

        for vehicle in vehicles:
            if vehicle.is_expired():
                message = f"Vehicle {vehicle.registration_number} has expired on {vehicle.expiry_date}."
                reminder_type = Reminder.INSURANCE  # Change this if needed

            elif vehicle.is_near_expiry() and not vehicle.near_expiry_notified:
                message = f"Vehicle {vehicle.registration_number} is expiring soon on {vehicle.expiry_date}."
                reminder_type = Reminder.INSURANCE  # Change this if needed
                vehicle.near_expiry_notified = True  # Mark as notified to avoid duplicate reminders
                vehicle.save()

            else:
                continue  # Skip vehicles that are not near expiry or expired

            Reminder.objects.create(
                vehicle=vehicle,
                reminder_date=today,
                type=reminder_type,
                status=Reminder.PENDING,
                message=message,
                is_read=False
            )

        self.stdout.write(self.style.SUCCESS("Vehicle expiry reminders checked and updated."))
