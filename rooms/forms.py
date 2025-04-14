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
        fields = ['check_in_date', 'check_out_date']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price_per_night', 'status']