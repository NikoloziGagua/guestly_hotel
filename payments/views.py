# payments/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import manager_required
from .models import SalaryRecord

#login_required
#manager_required
def salary_records_view(request):
    """
    Displays a list of all salary records.
    Managers can view the payment history for tasks completed by staff.
    """
    records = SalaryRecord.objects.all().order_by('-completed_at')
    context = {
        'records': records,
        'welcome_message': f"Salary Records - {request.user.username}"
    }
    return render(request, 'payments/salary_records.html', context)
