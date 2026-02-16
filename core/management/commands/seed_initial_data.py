from django.core.management.base import BaseCommand

from assignments.models import AssignmentReason
from core.models import Category, Location, Status
from consumables.models import Warehouse

LOCATIONS = [
    'Direccion Tecnica',
    'Secretaria',
    'LabStat',
    'Direccion Academica',
    'Direccion ejecutiva academica',
    'Direccion administrativa',
    'direccion ejecutiva administrativa',
    'datacenter',
    'almacen equipos informaticos',
    'almacen general',
    'laboratorio 1',
    'laboratorio 2',
    'laboratorio 3',
    'laboratorio 4',
    'cocina',
    'caseta de seguridad',
    'hall',
    'pasillo piso 1',
    'pasillo piso 2',
    'recepcion',
    'azotea',
]

CATEGORIES = [
    'CPU',
    'Laptop',
    'Server',
    'Switch',
    'Access Point',
    'Printer',
    'Teleconference',
    'Security Camera',
    'Projector',
    'Interactive Whiteboard',
    'Air Conditioner',
    'Biometric Clock',
    'Tablet',
    'Sound Console',
    'Webcam',
    'Headphones',
    'Microphone',
    'PC Speakers',
    'Monitor',
    'Keyboard',
]

STATUSES = ['Available', 'Assigned', 'Maintenance', 'Decommissioned']
WAREHOUSES = ['almacen equipos informaticos', 'almacen general']
ASSIGNMENT_REASONS = ['Initial assignment', 'Rotation', 'Replacement', 'Return']


class Command(BaseCommand):
    help = 'Load locations, categories, statuses and warehouses'

    def handle(self, *args, **options):
        for exact_name in LOCATIONS:
            Location.objects.get_or_create(exact_name=exact_name)
        for name in CATEGORIES:
            Category.objects.get_or_create(name=name)
        for name in STATUSES:
            Status.objects.get_or_create(name=name)
        for name in WAREHOUSES:
            Warehouse.objects.get_or_create(name=name)
        for name in ASSIGNMENT_REASONS:
            AssignmentReason.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Initial catalog data loaded.'))
