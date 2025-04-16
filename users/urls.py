from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    # Authentication and registration URLs
    path('users/main/', TemplateView.as_view(template_name='users/main.html'), name='main'),
    path('users/register/', views.register, name='register'),
    path('users/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Role-based dashboard URLs - Different views for different user roles
    path('dashboard/', views.role_based_redirect, name='role_redirect'),  # Smart redirect based on role
    path('dashboard/guest/', views.guest_dashboard, name='guest_dashboard'),
    path('dashboard/receptionist/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('dashboard/housekeeping/', views.housekeeping_dashboard, name='housekeeping_dashboard'),
    path('dashboard/room_service/', views.room_service_dashboard, name='room_service_dashboard'),
    
    # Manager-specific URLs - Control panel and administrative functions
    path('dashboard/manager/control/', views.manager_control_panel, name='manager_control_panel'),
    path('manager/billing/', views.billing_dashboard, name='billing_dashboard'),
    path('manager/reports/', views.manager_reports, name='manager_reports'),
    
    # Booking and user management URLs
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('manager/bookings/', views.view_all_bookings, name='view_all_bookings'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/add/', views.add_user, name='add_user'),
    path('manager/users/', views.view_all_users, name='view_all_users'),
    path('manager/roles/assign/', views.assign_user_role, name='assign_user_role'),
    
    # Development tools
    path('toggle-dev-mode/', views.toggle_dev_mode, name='toggle_dev_mode'),
]
