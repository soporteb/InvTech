from django.contrib.auth import get_user_model
from django.test import TestCase

from assignments.models import AssetAssignment, AssignmentReason
from assignments.services import reassign_asset, return_asset
from assets.models import Asset
from core.models import Category, Location, Status
from employees.models import Employee


class AssignmentServiceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='u1')
        self.location = Location.objects.create(exact_name='Direccion Tecnica')
        self.category = Category.objects.create(name='CPU')
        self.status = Status.objects.create(name='Available')
        self.asset = Asset.objects.create(category=self.category, location=self.location, status=self.status)
        self.reason = AssignmentReason.objects.create(name='Initial')
        self.reason2 = AssignmentReason.objects.create(name='Rotation')
        self.employee1 = Employee.objects.create(dni='11111111', names='Emp 1', worker_type=Employee.WorkerType.CAS)
        self.employee2 = Employee.objects.create(dni='22222222', names='Emp 2', worker_type=Employee.WorkerType.NOMBRADO)

    def test_reassign_closes_previous_and_creates_new(self):
        reassign_asset(asset=self.asset, new_employee=self.employee1, reason=self.reason, created_by=self.user)
        reassign_asset(asset=self.asset, new_employee=self.employee2, reason=self.reason2, created_by=self.user)
        assignments = AssetAssignment.objects.filter(asset=self.asset).order_by('created_at')
        self.assertEqual(assignments.count(), 2)
        self.assertIsNotNone(assignments.first().end_date)
        self.assertIsNone(assignments.last().end_date)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.responsible_employee_id, self.employee2.id)

    def test_return_unassign(self):
        reassign_asset(asset=self.asset, new_employee=self.employee1, reason=self.reason, created_by=self.user)
        return_asset(asset=self.asset, reason=self.reason2, created_by=self.user)
        self.asset.refresh_from_db()
        self.assertIsNone(self.asset.responsible_employee_id)
        active = AssetAssignment.objects.filter(asset=self.asset, end_date__isnull=True).count()
        self.assertEqual(active, 0)
