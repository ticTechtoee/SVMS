from datetime import date, timedelta
from vehicleApp.models import Vehicle, MaintenanceInterval, MaintenanceTask, VehicleMaintenanceSchedule
from reminderApp.models import Reminder

# Select an existing vehicle (create one if needed)
vehicle = Vehicle.objects.first()  # Change this if needed

# Create a maintenance interval
interval, _ = MaintenanceInterval.objects.get_or_create(
    name="Oil Change", interval_km=5000, description="Routine oil change"
)

# Create a maintenance task
task, _ = MaintenanceTask.objects.get_or_create(
    name="Change Engine Oil", description="Replace old engine oil", default_duration=30, cost_estimate=50.00
)

# Create upcoming maintenance (within 7 days)
upcoming_schedule = VehicleMaintenanceSchedule.objects.create(
    vehicle=vehicle,
    interval=interval,
    task=task,
    scheduled_date=date.today() + timedelta(days=5),
    status='pending'
)

# Create an expired maintenance (in the past)
expired_schedule = VehicleMaintenanceSchedule.objects.create(
    vehicle=vehicle,
    interval=interval,
    task=task,
    scheduled_date=date.today() - timedelta(days=3),
    status='pending'
)

print("Test data created successfully!")
