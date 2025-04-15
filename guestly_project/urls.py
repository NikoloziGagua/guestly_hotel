"""
Main URL configuration for the Guestly project.
This module handles the routing of all app-specific URLs and serves media files in debug mode.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Main URL patterns for the project
urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    # User management and authentication URLs
    path('users/', include('users.urls')),
    # Room management and booking URLs
    path('rooms/', include('rooms.urls')),
    # Hotel services URLs
    path('services/', include('services.urls')),
    # Payment and salary management URLs
    path('payments/', include('payments.urls')),
]

# Serve media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)