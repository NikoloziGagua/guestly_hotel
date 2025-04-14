# users/admin.py
from django.contrib import admin
from .models import CustomUser  # Adjust import paths as needed
from django.contrib.auth.admin import UserAdmin

# Your existing CustomUserAdmin definition...
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
