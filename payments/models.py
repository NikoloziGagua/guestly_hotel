
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

ROLE_CHOICES = [
    ('receptionist', 'Receptionist'),
    ('housekeeping', 'Housekeeping'),
    ('room_service', 'Room Service'),
]

class SalaryRate(models.Model):
    """
    Defines the fixed salary rate per completed task for each staff role.
    Only an admin can change these rates.
    """
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        unique=True,
        help_text="Staff role to which this rate applies."
    )
    rate = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        help_text="Salary per completed task for this role."
    )

    def __str__(self):
        return f"{self.get_role_display()}: {self.rate}"

class SalaryRecord(models.Model):
    """
    Logs each completed task payment.
    The salary is assigned by role and is fixed per task.
    """
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text="The staff role that completed the task."
    )
    amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        help_text="The payment amount for the completed task."
    )
    completed_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of task completion.")
    description = models.TextField(blank=True, help_text="Optional description of the completed task.")

    def __str__(self):
        return f"{self.get_role_display()} - {self.amount} on {self.completed_at.strftime('%Y-%m-%d %H:%M:%S')}"

