# Forms for room and booking management

from django import forms
from .models import Booking
from .models import Room

class BookingForm(forms.ModelForm):
    """
    Form for creating a booking.
    This form allows a guest to select check-in and check-out dates.
    """
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']  # Only date fields are exposed to users

class RoomForm(forms.ModelForm):
    """
    Form for room management.
    Used by managers to create and edit room details.
    """
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price_per_night', 'status']  # All room fields are exposed to managers