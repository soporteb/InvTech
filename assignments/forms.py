from django import forms

from employees.models import Employee

from .models import AssignmentReason


class ReassignForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.filter(is_active=True).order_by('names'))
    reason = forms.ModelChoiceField(queryset=AssignmentReason.objects.all().order_by('name'))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))


class ReturnAssetForm(forms.Form):
    reason = forms.ModelChoiceField(queryset=AssignmentReason.objects.all().order_by('name'))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
