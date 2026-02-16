from django.conf import settings
from django.db import models

from assets.models import Asset
from employees.models import Employee


class AssignmentReason(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class AssetAssignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='assignments')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='asset_assignments')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    reason = models.ForeignKey(AssignmentReason, on_delete=models.PROTECT, related_name='assignments')
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return f'{self.asset_id} -> {self.employee_id}'
