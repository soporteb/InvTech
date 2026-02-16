from django.db import models


class Employee(models.Model):
    class WorkerType(models.TextChoices):
        NOMBRADO = 'NOMBRADO', 'Nombrado'
        CAS = 'CAS', 'CAS'
        LOCADOR = 'LOCADOR', 'Locador'
        PRACTICANTE = 'PRACTICANTE', 'Practicante'

    dni = models.CharField(max_length=20, unique=True)
    names = models.CharField(max_length=255)
    worker_type = models.CharField(max_length=20, choices=WorkerType.choices)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['names']

    def __str__(self):
        return f'{self.names} ({self.dni})'
