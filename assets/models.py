from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models import Category, Location, Status
from employees.models import Employee


class Asset(models.Model):
    class OwnershipType(models.TextChoices):
        INSTITUTION = 'INSTITUTION', 'Institution'
        PROVIDER = 'PROVIDER', 'Provider'

    CONTROL_PATRIMONIAL_REQUIRED = {
        'teleconference',
        'projector',
        'interactive whiteboard',
        'air conditioner',
        'biometric clock',
        'tablet',
        'sound console',
    }
    INTERNAL_TAG_REQUIRED_ON_CREATE = {
        'webcam',
        'headphones',
        'microphone',
        'pc speakers',
    }

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='assets')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='assets')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='assets')
    observations = models.TextField(blank=True)

    control_patrimonial = models.CharField(max_length=120, unique=True, null=True, blank=True)
    serial = models.CharField(max_length=120, unique=True, null=True, blank=True)
    asset_tag_internal = models.CharField(max_length=120, unique=True, null=True, blank=True)

    ownership_type = models.CharField(
        max_length=20,
        choices=OwnershipType.choices,
        default=OwnershipType.INSTITUTION,
    )
    provider_name = models.CharField(max_length=255, blank=True)
    responsible_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responsible_assets',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        super().clean()
        errors = {}

        if self.responsible_employee and self.responsible_employee.worker_type not in {
            Employee.WorkerType.NOMBRADO,
            Employee.WorkerType.CAS,
        }:
            errors['responsible_employee'] = 'Responsible employee must be NOMBRADO or CAS.'

        category_name = (self.category.name if self.category_id and self.category else '').strip().lower()

        if category_name in self.CONTROL_PATRIMONIAL_REQUIRED and not self.control_patrimonial:
            errors['control_patrimonial'] = 'This category requires control_patrimonial.'

        if self._state.adding and category_name in self.INTERNAL_TAG_REQUIRED_ON_CREATE and not self.asset_tag_internal:
            errors['asset_tag_internal'] = 'This category requires asset_tag_internal at creation.'

        if self.ownership_type == self.OwnershipType.PROVIDER and 'camera' in category_name:
            if self.control_patrimonial:
                errors['control_patrimonial'] = 'Provider-owned cameras must not have control_patrimonial.'
            if not self.provider_name:
                errors['provider_name'] = 'Provider-owned cameras require provider_name.'

        if errors:
            raise ValidationError(errors)

    @property
    def has_padlock(self) -> bool:
        return bool(getattr(self, 'sensitive_data', None) and self.sensitive_data.cpu_padlock_key)

    @property
    def has_license(self) -> bool:
        sensitive_has_license = bool(getattr(self, 'sensitive_data', None) and self.sensitive_data.license_key)
        model_has_license = self.software_licenses.filter(assignment__is_active=True).exists()
        return sensitive_has_license or model_has_license

    def __str__(self):
        return f'{self.category} - {self.serial or self.asset_tag_internal or self.pk}'


class AssetSensitiveData(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='sensitive_data')
    cpu_padlock_key = models.CharField(max_length=255, blank=True)
    license_key = models.CharField(max_length=255, blank=True)
    admin_secret_note = models.TextField(blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_sensitive_assets',
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Sensitive data for asset {self.asset_id}'


class AssetEvent(models.Model):
    class EventType(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        UPDATED = 'UPDATED', 'Updated'
        ASSIGNED = 'ASSIGNED', 'Assigned'
        UNASSIGNED = 'UNASSIGNED', 'Unassigned'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=40, choices=EventType.choices)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=255)
    details_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.asset_id} - {self.event_type}'


class AssetCategoryBoundModel(models.Model):
    ALLOWED_CATEGORIES = set()

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if not self.ALLOWED_CATEGORIES:
            return
        category_name = self.asset.category.name.strip().lower()
        if category_name not in self.ALLOWED_CATEGORIES:
            raise ValidationError({'asset': f'Invalid category {self.asset.category.name} for {self.__class__.__name__}.'})


class ComputerSpecs(AssetCategoryBoundModel):
    ALLOWED_CATEGORIES = {'cpu', 'laptop', 'server'}

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='computer_specs')
    model_name = models.CharField(max_length=150)
    processor = models.CharField(max_length=150)
    cpu_speed = models.CharField(max_length=80, blank=True)
    ram_total_gb = models.PositiveIntegerField(default=0)
    ram_slots_total = models.PositiveIntegerField(default=0)
    domain = models.CharField(max_length=150, blank=True)
    dns1 = models.GenericIPAddressField(blank=True, null=True)
    dns2 = models.GenericIPAddressField(blank=True, null=True)
    host = models.CharField(max_length=150, blank=True)
    mac = models.CharField(max_length=50, blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    os_name = models.CharField(max_length=150, blank=True)
    antivirus_name = models.CharField(max_length=150, blank=True)
    padlock_present = models.BooleanField(default=False)


class SwitchDetails(AssetCategoryBoundModel):
    ALLOWED_CATEGORIES = {'switch'}

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='switch_details')
    brand = models.CharField(max_length=120)
    model = models.CharField(max_length=120)
    ip = models.GenericIPAddressField(blank=True, null=True)
    managed_by_text = models.CharField(max_length=255)
    switch_type = models.CharField(max_length=120, blank=True)


class AccessPointDetails(AssetCategoryBoundModel):
    ALLOWED_CATEGORIES = {'access point'}

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='access_point_details')
    brand = models.CharField(max_length=120)
    model = models.CharField(max_length=120)
    ip = models.GenericIPAddressField(blank=True, null=True)
    managed_by_text = models.CharField(max_length=255)
    ap_type = models.CharField(max_length=120, blank=True)
    standalone_server = models.BooleanField(default=False)


class PrinterDetails(AssetCategoryBoundModel):
    ALLOWED_CATEGORIES = {'printer'}

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='printer_details')
    brand = models.CharField(max_length=120)
    model = models.CharField(max_length=120)
    ip = models.GenericIPAddressField(blank=True, null=True)
    associated_email = models.EmailField(blank=True)


class TeleconferenceDetails(AssetCategoryBoundModel):
    ALLOWED_CATEGORIES = {'teleconference'}

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='teleconference_details')
    brand = models.CharField(max_length=120)
    model = models.CharField(max_length=120)
    ip = models.GenericIPAddressField(blank=True, null=True)


class SecurityCameraDetails(AssetCategoryBoundModel):
    ALLOWED_CATEGORIES = {'security camera'}

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='security_camera_details')
    brand = models.CharField(max_length=120)
    model = models.CharField(max_length=120)
    ip = models.GenericIPAddressField(blank=True, null=True)


class PeripheralDetails(AssetCategoryBoundModel):
    ALLOWED_CATEGORIES = {'monitor', 'keyboard'}

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='peripheral_details')
    brand = models.CharField(max_length=120)
    model = models.CharField(max_length=120, blank=True)
    linked_asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_peripherals')


class SoftwareLicense(models.Model):
    name = models.CharField(max_length=150)
    vendor = models.CharField(max_length=150, blank=True)
    seats = models.PositiveIntegerField(default=1)
    expiration_date = models.DateField(null=True, blank=True)
    assets = models.ManyToManyField(Asset, through='SoftwareLicenseAssignment', related_name='software_licenses')

    class Meta:
        unique_together = ('name', 'vendor')


class LicenseSensitiveData(models.Model):
    license = models.OneToOneField(SoftwareLicense, on_delete=models.CASCADE, related_name='sensitive_data')
    secret_key = models.CharField(max_length=255)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class SoftwareLicenseAssignment(models.Model):
    license = models.ForeignKey(SoftwareLicense, on_delete=models.CASCADE, related_name='assignment')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='license_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('license', 'asset')


class AssetOperation(models.Model):
    class OperationType(models.TextChoices):
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'
        REPLACEMENT = 'REPLACEMENT', 'Replacement'
        DECOMMISSION = 'DECOMMISSION', 'Decommission'

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='operations')
    operation_type = models.CharField(max_length=20, choices=OperationType.choices)
    performed_at = models.DateTimeField(auto_now_add=True)
    justification = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-performed_at']

    def clean(self):
        super().clean()
        if self.operation_type == self.OperationType.REPLACEMENT and not self.justification:
            raise ValidationError({'justification': 'Replacement requires justification.'})

    def __str__(self):
        return f"{self.asset_id} - {self.operation_type}"
