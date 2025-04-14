# rooms/models.py

from django.db import models
from django.utils import timezone

# Your existing choices...
ROOM_STATUS_CHOICES = [
    ('available', 'Available'),
    ('occupied', 'Occupied'),
    ('needs_cleaning', 'Needs Cleaning'),
    ('maintenance', 'Under Maintenance'),
]

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=[('single', 'Single'), ('double', 'Double'), ('suite', 'Suite')])
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='available')
    dirty_since = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        # Return a human-friendly description of the room.
        return f"Room {self.room_number} ({self.get_room_type_display()})"

    def mark_as_occupied(self):
        """
        Mark this room as 'occupied' when a booking is processed.
        """
        self.status = 'occupied'
        self.save()  # Save changes to the database

    def mark_as_needs_cleaning(self):
        """
        Mark this room as needing cleaning, and record the current time.
        Typically called during check-out.
        """
        self.status = 'needs_cleaning'
        self.dirty_since = timezone.now()  # Record the time when room became dirty
        self.save()

    def mark_as_cleaned(self):
        """
        Mark this room as cleaned.
        Only allowed if the room was previously marked as needing cleaning.
        """
        if self.status == 'needs_cleaning':
            self.status = 'available'
            self.dirty_since = None  # Clear the timestamp as the room is now clean
            self.save()

# rooms/models.py (continued)

from django.conf import settings

BOOKING_STATUS_CHOICES = [
    ('reserved', 'Reserved'),
    ('checked_in', 'Checked-in'),
    ('checked_out', 'Checked-out'),
    ('cancelled', 'Cancelled'),
]

class Booking(models.Model):
    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='reserved')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Provides a summary of the booking with guest, room number, and check-in date.
        return f"Booking for {self.guest.username} in Room {self.room.room_number} on {self.check_in_date}"

    def calculate_total_price(self):
        """
        Calculate the total cost of this booking based on the room's price and the number of nights.
        """
        nights = (self.check_out_date - self.check_in_date).days
        return self.room.price_per_night * nights

    def process_booking(self):
        """
        Process the booking by calculating the total price and updating the room status.
        This method centralizes the booking logic.
        """
        self.total_price = self.calculate_total_price()  # Compute cost
        self.save()  # Save booking details first
        self.room.mark_as_occupied()  # Update the room status to reflect the new booking

    def check_in(self):
        """
        Handle the check-in process:
         - Ensure the booking is in 'reserved' status.
         - Change the booking status to 'checked_in'.
         - Mark the associated room as occupied.
        """
        if self.status != 'reserved':
            raise ValueError("Booking must be in 'reserved' state to check in.")
        self.status = 'checked_in'
        self.save()
        self.room.mark_as_occupied()  # Room should be occupied during check-in

    def check_out(self):
        """
        Handle the check-out process:
         - Ensure the booking is currently checked in.
         - Change the booking status to 'checked_out'.
         - Mark the room as needing cleaning.
        """
        if self.status != 'checked_in':
            raise ValueError("Booking must be checked in to check out.")
        self.status = 'checked_out'
        self.save()
        self.room.mark_as_needs_cleaning()  # Room now needs cleaning after check-out
