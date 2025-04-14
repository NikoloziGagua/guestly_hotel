# payments/urls.py

from django.urls import path
from .views import salary_records_view

urlpatterns = [
    path('salary-records/', salary_records_view, name='salary_records'),
]
