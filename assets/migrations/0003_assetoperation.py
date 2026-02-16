from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0002_phase2_detail_models_and_licenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_type', models.CharField(choices=[('MAINTENANCE', 'Maintenance'), ('REPLACEMENT', 'Replacement'), ('DECOMMISSION', 'Decommission')], max_length=20)),
                ('performed_at', models.DateTimeField(auto_now_add=True)),
                ('justification', models.TextField(blank=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='assets.asset')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-performed_at']},
        ),
    ]
