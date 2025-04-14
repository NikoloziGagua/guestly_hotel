# Generated by Django 5.1.7 on 2025-04-05 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_salary', models.DecimalField(decimal_places=2, default=0.0, help_text='Base salary for the staff member.', max_digits=10)),
                ('per_task_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Additional payment per completed task (if applicable).', max_digits=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff_payment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
