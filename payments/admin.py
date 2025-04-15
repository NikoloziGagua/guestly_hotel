# payments/admin.py

"""
Admin interface configuration for the payments application.
Defines how payment-related models are displayed and managed in the Django admin interface.
"""
from django.contrib import admin
from .models import SalaryRate, SalaryRecord

@admin.register(SalaryRate)
class SalaryRateAdmin(admin.ModelAdmin):
    """Admin interface for managing salary rates by role"""
    list_display = ('role', 'rate')
    search_fields = ('role',)

@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    """Admin interface for managing salary payment records"""
    list_display = ('role', 'amount', 'completed_at', 'description')
    list_filter = ('role', 'completed_at')
    search_fields = ('role', 'description')
