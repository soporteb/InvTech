from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CartridgeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=120)),
                ('model', models.CharField(max_length=120)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
            options={'ordering': ['brand', 'model'], 'unique_together': {('brand', 'model')}},
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('cartridge_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_items', to='consumables.cartridgemodel')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_items', to='consumables.warehouse')),
            ],
            options={'ordering': ['warehouse__name'], 'unique_together': {('cartridge_model', 'warehouse')}},
        ),
    ]
