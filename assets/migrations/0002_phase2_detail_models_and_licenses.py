from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftwareLicense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('vendor', models.CharField(blank=True, max_length=150)),
                ('seats', models.PositiveIntegerField(default=1)),
                ('expiration_date', models.DateField(blank=True, null=True)),
            ],
            options={'unique_together': {('name', 'vendor')}},
        ),
        migrations.CreateModel(
            name='AccessPointDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=120)),
                ('model', models.CharField(max_length=120)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('managed_by_text', models.CharField(max_length=255)),
                ('ap_type', models.CharField(blank=True, max_length=120)),
                ('standalone_server', models.BooleanField(default=False)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='access_point_details', to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='ComputerSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=150)),
                ('processor', models.CharField(max_length=150)),
                ('cpu_speed', models.CharField(blank=True, max_length=80)),
                ('ram_total_gb', models.PositiveIntegerField(default=0)),
                ('ram_slots_total', models.PositiveIntegerField(default=0)),
                ('domain', models.CharField(blank=True, max_length=150)),
                ('dns1', models.GenericIPAddressField(blank=True, null=True)),
                ('dns2', models.GenericIPAddressField(blank=True, null=True)),
                ('host', models.CharField(blank=True, max_length=150)),
                ('mac', models.CharField(blank=True, max_length=50)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('os_name', models.CharField(blank=True, max_length=150)),
                ('antivirus_name', models.CharField(blank=True, max_length=150)),
                ('padlock_present', models.BooleanField(default=False)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='computer_specs', to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='PrinterDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=120)),
                ('model', models.CharField(max_length=120)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('associated_email', models.EmailField(blank=True, max_length=254)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='printer_details', to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='SecurityCameraDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=120)),
                ('model', models.CharField(max_length=120)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='security_camera_details', to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='SwitchDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=120)),
                ('model', models.CharField(max_length=120)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('managed_by_text', models.CharField(max_length=255)),
                ('switch_type', models.CharField(blank=True, max_length=120)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='switch_details', to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='TeleconferenceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=120)),
                ('model', models.CharField(max_length=120)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teleconference_details', to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareLicenseAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='license_assignments', to='assets.asset')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='assets.softwarelicense')),
            ],
            options={'unique_together': {('license', 'asset')}},
        ),
        migrations.CreateModel(
            name='PeripheralDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=120)),
                ('model', models.CharField(blank=True, max_length=120)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='peripheral_details', to='assets.asset')),
                ('linked_asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='linked_peripherals', to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='LicenseSensitiveData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_key', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('license', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sensitive_data', to='assets.softwarelicense')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='softwarelicense',
            name='assets',
            field=models.ManyToManyField(related_name='software_licenses', through='assets.SoftwareLicenseAssignment', to='assets.asset'),
        ),
    ]
