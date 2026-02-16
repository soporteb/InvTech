from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consumables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('IN', 'IN'), ('OUT', 'OUT'), ('TRANSFER', 'TRANSFER'), ('ADJUST', 'ADJUST'), ('SCRAP', 'SCRAP')], max_length=10)),
                ('quantity', models.PositiveIntegerField()),
                ('reason', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cartridge_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movements', to='consumables.cartridgemodel')),
                ('from_warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movements_out', to='consumables.warehouse')),
                ('to_warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movements_in', to='consumables.warehouse')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
