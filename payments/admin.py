# payments/admin.py

from django.contrib import admin
from .models import SalaryRate, SalaryRecord

@admin.register(SalaryRate)
class SalaryRateAdmin(admin.ModelAdmin):
    list_display = ('role', 'rate')
    search_fields = ('role',)

@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    list_display = ('role', 'amount', 'completed_at', 'description')
    list_filter = ('role', 'completed_at')
    search_fields = ('role', 'description')
