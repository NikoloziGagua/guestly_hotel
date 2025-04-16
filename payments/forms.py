from django import forms
from .models import SalaryRate, SalaryRecord
from django.conf import settings

class SalaryRateForm(forms.ModelForm):
    """Form for managing salary rates for different roles.
    
    This form allows setting and updating hourly rates for various job roles.
    The role field is disabled to prevent modification once created.
    """
    class Meta:
        model = SalaryRate
        fields = ['role', 'rate']
        widgets = {
            'role': forms.Select(attrs={'disabled': True})  # Role field is disabled to prevent changes
        }

class SalaryRecordForm(forms.ModelForm):
    """Form for creating salary records/time entries.
    
    Used to log work hours with a specific role and description
    of the work performed.
    """
    class Meta:
        model = SalaryRecord
        fields = ['role', 'description']  # Role selection and work description