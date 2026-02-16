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
