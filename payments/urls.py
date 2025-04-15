# payments/urls.py

"""
URL patterns for the payments application.
Defines routes for salary and payment management features.
"""
from django.urls import path
from .views import salary_records_view

# URL patterns specific to payment functionality
urlpatterns = [
    # Route for viewing salary records (manager access only)
    path('salary-records/', salary_records_view, name='salary_records'),
]
