from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from accounts.roles import ROLE_ADMIN, ROLE_VIEWER
from assets.models import (
    Asset,
    AssetSensitiveData,
    ComputerSpecs,
    SoftwareLicense,
    SoftwareLicenseAssignment,
)
from assets.services import build_asset_context_for_user
from core.models import Category, Location, Status
from employees.models import Employee


class AssetModelTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(exact_name='Direccion Tecnica')
        self.status = Status.objects.create(name='Available')
        self.cpu = Category.objects.create(name='CPU')
        self.teleconference = Category.objects.create(name='Teleconference')
        self.projector = Category.objects.create(name='Projector')
        self.webcam = Category.objects.create(name='Webcam')
        self.camera = Category.objects.create(name='Security Camera')

    def create_asset(self, category, **kwargs):
        payload = {
            'category': category,
            'location': self.location,
            'status': self.status,
        }
        payload.update(kwargs)
        return Asset.objects.create(**payload)

    def test_serial_unique_when_present(self):
        self.create_asset(category=self.cpu, serial='ABC123')
        with self.assertRaises(IntegrityError):
            self.create_asset(category=self.cpu, serial='ABC123')

    def test_responsible_must_be_nombrado_or_cas(self):
        employee = Employee.objects.create(dni='12345678', names='Locador User', worker_type=Employee.WorkerType.LOCADOR)
        asset = Asset(
            category=self.cpu,
            location=self.location,
            status=self.status,
            responsible_employee=employee,
        )
        with self.assertRaises(ValidationError):
            asset.full_clean()

    def test_asset_has_no_area_field_and_uses_location(self):
        self.assertIn('location', [f.name for f in Asset._meta.fields])
        self.assertNotIn('area', [f.name for f in Asset._meta.fields])

    def test_teleconference_requires_control_patrimonial(self):
        asset = Asset(category=self.teleconference, location=self.location, status=self.status)
        with self.assertRaises(ValidationError):
            asset.full_clean()

    def test_projector_requires_control_patrimonial(self):
        asset = Asset(category=self.projector, location=self.location, status=self.status)
        with self.assertRaises(ValidationError):
            asset.full_clean()

    def test_webcam_requires_internal_tag_on_create(self):
        asset = Asset(category=self.webcam, location=self.location, status=self.status)
        with self.assertRaises(ValidationError):
            asset.full_clean()

    def test_provider_camera_requires_provider_and_null_control_patrimonial(self):
        asset = Asset(
            category=self.camera,
            location=self.location,
            status=self.status,
            ownership_type=Asset.OwnershipType.PROVIDER,
            control_patrimonial='CP-1',
        )
        with self.assertRaises(ValidationError):
            asset.full_clean()

        valid = Asset(
            category=self.camera,
            location=self.location,
            status=self.status,
            ownership_type=Asset.OwnershipType.PROVIDER,
            provider_name='CameraCo',
        )
        valid.full_clean()


class SensitiveDataVisibilityTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Laptop')
        self.location = Location.objects.create(exact_name='Secretaria')
        self.status = Status.objects.create(name='Assigned')
        self.asset = Asset.objects.create(category=self.category, location=self.location, status=self.status)
        AssetSensitiveData.objects.create(
            asset=self.asset,
            cpu_padlock_key='PADLOCK-SECRET',
            license_key='LICENSE-SECRET',
            admin_secret_note='TOP SECRET',
        )
        User = get_user_model()
        self.admin = User.objects.create_user(username='admin', password='x')
        self.viewer = User.objects.create_user(username='viewer', password='x')

        admin_group, _ = Group.objects.get_or_create(name=ROLE_ADMIN)
        viewer_group, _ = Group.objects.get_or_create(name=ROLE_VIEWER)
        self.admin.groups.add(admin_group)
        self.viewer.groups.add(viewer_group)

    def test_non_admin_context_never_includes_sensitive_values(self):
        context = build_asset_context_for_user(self.viewer, self.asset)
        self.assertEqual(context['padlock'], 'Yes')
        self.assertEqual(context['license'], 'Yes')
        self.assertNotIn('sensitive', context)

    def test_admin_context_includes_sensitive_values(self):
        context = build_asset_context_for_user(self.admin, self.asset)
        self.assertIn('sensitive', context)
        self.assertEqual(context['sensitive']['cpu_padlock_key'], 'PADLOCK-SECRET')

    def test_license_indicator_works_with_software_license_assignment(self):
        AssetSensitiveData.objects.filter(asset=self.asset).update(license_key='')
        license_item = SoftwareLicense.objects.create(name='Office', vendor='Contoso', seats=10)
        SoftwareLicenseAssignment.objects.create(license=license_item, asset=self.asset, is_active=True)

        viewer_context = build_asset_context_for_user(self.viewer, self.asset)
        self.assertEqual(viewer_context['license'], 'Yes')
        self.assertNotIn('sensitive', viewer_context)


class DetailModelValidationTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(exact_name='LabStat')
        self.status = Status.objects.create(name='Operational')
        self.cpu_category = Category.objects.create(name='CPU')
        self.switch_category = Category.objects.create(name='Switch')
        self.cpu_asset = Asset.objects.create(category=self.cpu_category, location=self.location, status=self.status)
        self.switch_asset = Asset.objects.create(category=self.switch_category, location=self.location, status=self.status)

    def test_computer_specs_accepts_cpu_category(self):
        specs = ComputerSpecs(
            asset=self.cpu_asset,
            model_name='Optiplex',
            processor='Intel i7',
        )
        specs.full_clean()

    def test_computer_specs_rejects_switch_category(self):
        specs = ComputerSpecs(
            asset=self.switch_asset,
            model_name='SWX',
            processor='N/A',
        )
        with self.assertRaises(ValidationError):
            specs.full_clean()
