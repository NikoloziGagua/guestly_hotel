# users/models.py

# users/models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'), 
        ('housekeeping', 'Housekeeping'),
        ('guest', 'Guest'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='guest'  # This is just the default, form selection should override
    )

    # ---------------------------
    # Helper methods for role checking
    # ---------------------------
    def is_guest(self):
        """Return True if the user is a guest."""
        return self.role == 'guest'

    def is_receptionist(self):
        """Return True if the user is a receptionist."""
        return self.role == 'receptionist'

    def is_housekeeping(self):
        """Return True if the user is a housekeeping staff."""
        return self.role == 'housekeeping'

    def is_manager(self):
        """Return True if the user is a manager."""
        return self.role == 'manager'

    def is_room_service(self):
        """Return True if the user is part of room service."""
        return self.role == 'room_service'

    # ---------------------------
    # Dashboard URL Helper
    # ---------------------------
    def get_dashboard_url(self):
        """
        Returns the appropriate dashboard URL name based on the user's role.
        This centralizes the redirection logic.
        """
        if self.is_guest():
            return 'guest_dashboard'
        elif self.is_receptionist():
            return 'receptionist_dashboard'
        elif self.is_housekeeping():
            return 'housekeeping_dashboard'
        elif self.is_manager():
            return 'manager_control_panel'
        elif self.is_room_service():
            return 'room_service_dashboard'
        # Default fallback, could be the login page
        return 'login'