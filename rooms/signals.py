from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Booking, Room

@receiver(post_delete, sender=Booking)
def update_room_status_on_booking_delete(sender, instance, **kwargs):
    """
    When a booking is deleted, this signal checks if the room has any other active bookings.
    If none, it updates the room's status to 'available'.
    """
    room = instance.room
    active_bookings = room.bookings.exclude(id=instance.id).exists()
    if not active_bookings:
        room.status = 'available'
        room.save()
