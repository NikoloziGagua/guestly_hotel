# URL configuration for the rooms application

from django.urls import path
from . import views
from.views import room_management_home
from django.urls import path, include

urlpatterns = [
    # Guest accessible URLs
    path('', views.room_list, name='room_list'),  # Display all available rooms
    path('book/<int:room_id>/', views.create_booking, name='create_booking'),  # Create new booking
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),  # Cancel existing booking
    
    # Receptionist URLs
    path('checkin/<int:booking_id>/', views.check_in_booking, name='check_in_booking'),  # Process check-in
    path('checkout/<int:booking_id>/', views.check_out_booking, name='check_out_booking'),  # Process check-out
    
    # Manager URLs
    path('manager/rooms/', room_management_home, name='room_management_home'),  # Room management dashboard
    path('manager/rooms/add/', views.add_room, name='add_room'),  # Add new room
    path('manager/rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),  # Edit existing room
    path('manager/rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),  # Delete room
]
