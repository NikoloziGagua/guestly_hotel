from django.urls import path
from . import views
from.views import room_management_home
from django.urls import path, include

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('book/<int:room_id>/', views.create_booking, name='create_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),  # ✅ Make sure this is here
    path('checkin/<int:booking_id>/', views.check_in_booking, name='check_in_booking'),
    path('checkout/<int:booking_id>/', views.check_out_booking, name='check_out_booking'),
    path('manager/rooms/', room_management_home, name='room_management_home'),
    path('manager/rooms/add/', views.add_room, name='add_room'),
    path('manager/rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('manager/rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),

]
