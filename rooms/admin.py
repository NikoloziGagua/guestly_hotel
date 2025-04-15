# Admin interface configurations for Room and Booking models

from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin interface configuration for Room model."""
    list_display = ('room_number', 'room_type', 'price_per_night', 'status')  # Fields shown in list view
    list_filter = ('room_type', 'status')  # Filters available in admin
    search_fields = ('room_number',)  # Fields that can be searched

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin interface configuration for Booking model."""
    list_display = ('guest', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price')
    list_filter = ('status', 'check_in_date', 'check_out_date')  # Date and status filters
    search_fields = ('guest__username', 'room__room_number')  # Search by guest or room number
