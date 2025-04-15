# Signal handlers for automated room status updates

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Booking, Room

@receiver(post_delete, sender=Booking)
def update_room_status_on_booking_delete(sender, instance, **kwargs):
    """
    Signal handler that updates room status when a booking is deleted.
    
    This ensures room availability is correctly maintained when bookings are removed.
    If the room has no other active bookings, its status is set to 'available'.
    
    """
    room = instance.room
    active_bookings = room.bookings.exclude(id=instance.id).exists()
    if not active_bookings:
        room.status = 'available'
        room.save()
