from django.core.management.base import BaseCommand
from datetime import date, timedelta
from vehicleApp.models import VehicleMaintenanceSchedule
from reminderApp.models import Reminder

class Command(BaseCommand):
    help = "Generate reminders for upcoming maintenance schedules"

    def handle(self, *args, **kwargs):
        today = date.today()
        upcoming_maintenance = VehicleMaintenanceSchedule.objects.filter(
            scheduled_date__gte=today, scheduled_date__lte=today + timedelta(days=7), status='pending'
        )
        expired_maintenance = VehicleMaintenanceSchedule.objects.filter(
            scheduled_date__lt=today, status='pending'
        )

        # Create reminders for upcoming maintenance
        for schedule in upcoming_maintenance:
            Reminder.objects.get_or_create(
                vehicle=schedule.vehicle,
                reminder_date=schedule.scheduled_date,
                type=Reminder.SERVICE,
                status=Reminder.PENDING
            )

        # Create reminders for expired maintenance
        for schedule in expired_maintenance:
            Reminder.objects.get_or_create(
                vehicle=schedule.vehicle,
                reminder_date=schedule.scheduled_date,
                type=Reminder.SERVICE,
                status=Reminder.PENDING
            )

        self.stdout.write(self.style.SUCCESS("Reminders generated successfully!"))
