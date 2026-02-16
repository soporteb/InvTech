from django.core.exceptions import ValidationError
from django.test import TestCase

from consumables.models import CartridgeModel, StockItem, StockMovement, Warehouse
from consumables.services import apply_stock_movement


class StockMovementTests(TestCase):
    def setUp(self):
        self.model = CartridgeModel.objects.create(brand='HP', model='85A')
        self.wh_a = Warehouse.objects.create(name='A')
        self.wh_b = Warehouse.objects.create(name='B')

    def test_prevent_negative_stock(self):
        with self.assertRaises(ValidationError):
            apply_stock_movement(
                cartridge_model=self.model,
                movement_type=StockMovement.MovementType.OUT,
                quantity=1,
                reason='issue',
                from_warehouse=self.wh_a,
            )

    def test_transfer_updates_both_warehouses(self):
        apply_stock_movement(
            cartridge_model=self.model,
            movement_type=StockMovement.MovementType.IN,
            quantity=10,
            reason='purchase',
            to_warehouse=self.wh_a,
        )
        apply_stock_movement(
            cartridge_model=self.model,
            movement_type=StockMovement.MovementType.TRANSFER,
            quantity=4,
            reason='move',
            from_warehouse=self.wh_a,
            to_warehouse=self.wh_b,
        )
        self.assertEqual(StockItem.objects.get(cartridge_model=self.model, warehouse=self.wh_a).quantity, 6)
        self.assertEqual(StockItem.objects.get(cartridge_model=self.model, warehouse=self.wh_b).quantity, 4)

    def test_movements_are_immutable(self):
        movement = apply_stock_movement(
            cartridge_model=self.model,
            movement_type=StockMovement.MovementType.IN,
            quantity=2,
            reason='purchase',
            to_warehouse=self.wh_a,
        )
        movement.reason = 'changed'
        with self.assertRaises(ValidationError):
            movement.save()
