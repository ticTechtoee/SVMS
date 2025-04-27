from django.core.management.base import BaseCommand
from datetime import date
from vehicleApp.models import VehicleServiceRecord, Vehicle, MaintenanceType
from reminderApp.models import Reminder

# Predefined maintenance intervals
MAINTENANCE_MILESTONES = {
    "A": [5000, 15000, 25000],
    "B": [10000, 30000, 50000],
    "C": [20000, 60000, 120000],
    "D": [40000, 80000],
}

class Command(BaseCommand):
    help = "Generate reminders for upcoming maintenance schedules based on mileage"

    def handle(self, *args, **kwargs):
        today = date.today()

        for vehicle in Vehicle.objects.all():
            # Get the last recorded maintenance for this vehicle
            last_service = VehicleServiceRecord.objects.filter(vehicle=vehicle).order_by('-mileage_at_service').first()

            if last_service:
                last_mileage = last_service.mileage_at_service
                category_code = last_service.maintenance_type.name  # ✅ Correct field now!

                if category_code in MAINTENANCE_MILESTONES:
                    milestones = MAINTENANCE_MILESTONES[category_code]
                    next_milestone = next((m for m in milestones if m > last_mileage), None)

                    if next_milestone:
                        # Create reminder only if it doesn't already exist
                        Reminder.objects.get_or_create(
                            vehicle=vehicle,
                            reminder_date=today,
                            type=Reminder.SERVICE,
                            status=Reminder.PENDING,
                        )


        self.stdout.write(self.style.SUCCESS("Maintenance reminders updated successfully!"))
