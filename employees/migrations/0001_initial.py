from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=20, unique=True)),
                ('names', models.CharField(max_length=255)),
                ('worker_type', models.CharField(choices=[('NOMBRADO', 'Nombrado'), ('CAS', 'CAS'), ('LOCADOR', 'Locador'), ('PRACTICANTE', 'Practicante')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=50)),
            ],
            options={'ordering': ['names']},
        ),
    ]
