from django.core.exceptions import ValidationError
from django.db import models


class CartridgeModel(models.Model):
    brand = models.CharField(max_length=120)
    model = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('brand', 'model')
        ordering = ['brand', 'model']

    def __str__(self):
        return f'{self.brand} {self.model}'


class Warehouse(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class StockItem(models.Model):
    cartridge_model = models.ForeignKey(CartridgeModel, on_delete=models.PROTECT, related_name='stock_items')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='stock_items')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('cartridge_model', 'warehouse')
        ordering = ['warehouse__name']

    def __str__(self):
        return f'{self.cartridge_model} @ {self.warehouse}: {self.quantity}'


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = 'IN', 'IN'
        OUT = 'OUT', 'OUT'
        TRANSFER = 'TRANSFER', 'TRANSFER'
        ADJUST = 'ADJUST', 'ADJUST'
        SCRAP = 'SCRAP', 'SCRAP'

    cartridge_model = models.ForeignKey(CartridgeModel, on_delete=models.PROTECT, related_name='movements')
    movement_type = models.CharField(max_length=10, choices=MovementType.choices)
    quantity = models.PositiveIntegerField()
    from_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='movements_out',
    )
    to_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='movements_in',
    )
    reason = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        super().clean()
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be positive.'})
        if self.movement_type in {self.MovementType.OUT, self.MovementType.SCRAP, self.MovementType.ADJUST} and not self.from_warehouse:
            raise ValidationError({'from_warehouse': 'from_warehouse is required.'})
        if self.movement_type in {self.MovementType.IN} and not self.to_warehouse:
            raise ValidationError({'to_warehouse': 'to_warehouse is required.'})
        if self.movement_type == self.MovementType.TRANSFER:
            if not self.from_warehouse or not self.to_warehouse:
                raise ValidationError('TRANSFER requires both from_warehouse and to_warehouse.')
            if self.from_warehouse_id == self.to_warehouse_id:
                raise ValidationError('TRANSFER warehouses must be different.')

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError('Stock movements are immutable. Use ADJUST for corrections.')
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.movement_type} {self.quantity} {self.cartridge_model}'
