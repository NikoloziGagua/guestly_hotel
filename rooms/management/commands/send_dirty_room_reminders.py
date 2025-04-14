from django.core.management.base import BaseCommand
from django.utils import timezone
from rooms.models import Room
from datetime import timedelta
from django.core.mail import send_mail  # or simply log the reminder
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends reminders for rooms that have been marked as needs_cleaning for over X hours.'

    def handle(self, *args, **kwargs):
        # Define the threshold (e.g., 1 hour)
        threshold = timezone.now() - timedelta(hours=1)
        # Query for rooms that are marked as needs_cleaning and have been so since before the threshold
        dirty_rooms = Room.objects.filter(status='needs_cleaning', dirty_since__lt=threshold)
        
        if dirty_rooms.exists():
            for room in dirty_rooms:
                message = f"Room {room.room_number} has been dirty since {room.dirty_since.strftime('%Y-%m-%d %H:%M:%S')}."
                self.stdout.write(self.style.WARNING(message))
                # Optionally, send an email reminder:
                # send_mail("Dirty Room Reminder",
                #           message,
                #           settings.DEFAULT_FROM_EMAIL,
                #           ["housekeeping@example.com"])
        else:
            self.stdout.write("No rooms require a reminder at this time.")
