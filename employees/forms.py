from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['dni', 'names', 'worker_type', 'is_active', 'email', 'phone']
