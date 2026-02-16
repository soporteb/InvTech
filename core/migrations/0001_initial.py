from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(blank=True, max_length=120)),
                ('floor', models.CharField(blank=True, max_length=120)),
                ('type', models.CharField(blank=True, max_length=120)),
                ('exact_name', models.CharField(max_length=150, unique=True)),
            ],
            options={'ordering': ['exact_name']},
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
            options={'ordering': ['name']},
        ),
    ]
