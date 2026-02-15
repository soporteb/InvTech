from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observations', models.TextField(blank=True)),
                ('control_patrimonial', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('serial', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('asset_tag_internal', models.CharField(blank=True, max_length=120, null=True, unique=True)),
                ('ownership_type', models.CharField(choices=[('INSTITUTION', 'Institution'), ('PROVIDER', 'Provider')], default='INSTITUTION', max_length=20)),
                ('provider_name', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assets', to='core.category')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assets', to='core.location')),
                ('responsible_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible_assets', to='employees.employee')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assets', to='core.status')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='AssetEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('CREATED', 'Created'), ('UPDATED', 'Updated'), ('ASSIGNED', 'Assigned'), ('UNASSIGNED', 'Unassigned'), ('MAINTENANCE', 'Maintenance')], max_length=40)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('summary', models.CharField(max_length=255)),
                ('details_json', models.JSONField(blank=True, default=dict)),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='assets.asset')),
            ],
            options={'ordering': ['-timestamp']},
        ),
        migrations.CreateModel(
            name='AssetSensitiveData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_padlock_key', models.CharField(blank=True, max_length=255)),
                ('license_key', models.CharField(blank=True, max_length=255)),
                ('admin_secret_note', models.TextField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sensitive_data', to='assets.asset')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_sensitive_assets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
