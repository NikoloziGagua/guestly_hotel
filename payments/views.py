"""
Views for handling payment-related operations in the Guestly system.
This module includes views for salary record management and payment processing.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import manager_required
from .models import SalaryRecord

# Require both login and manager status to access salary records
@login_required
@manager_required
def salary_records_view(request):
    """
    Displays a list of all salary records.
    """
    records = SalaryRecord.objects.all().order_by('-completed_at')
    context = {
        'records': records,
        'welcome_message': f"Salary Records - {request.user.username}"
    }
    return render(request, 'payments/salary_records.html', context)
