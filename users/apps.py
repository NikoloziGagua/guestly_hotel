"""Users app configuration module.

Defines the configuration for the users Django application.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration class for the users app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
