from django.core.exceptions import ValidationError
from django.db import transaction

from .models import StockItem, StockMovement


def _get_stock_item(cartridge_model, warehouse):
    item, _ = StockItem.objects.select_for_update().get_or_create(
        cartridge_model=cartridge_model,
        warehouse=warehouse,
        defaults={'quantity': 0},
    )
    return item


@transaction.atomic
def apply_stock_movement(*, cartridge_model, movement_type, quantity, reason, from_warehouse=None, to_warehouse=None, note=''):
    movement = StockMovement(
        cartridge_model=cartridge_model,
        movement_type=movement_type,
        quantity=quantity,
        reason=reason,
        from_warehouse=from_warehouse,
        to_warehouse=to_warehouse,
        note=note,
    )
    movement.full_clean()

    if movement_type in {StockMovement.MovementType.OUT, StockMovement.MovementType.SCRAP, StockMovement.MovementType.ADJUST}:
        source = _get_stock_item(cartridge_model, from_warehouse)
        if source.quantity < quantity:
            raise ValidationError('Insufficient stock for movement.')
        source.quantity -= quantity
        source.save(update_fields=['quantity'])

    if movement_type in {StockMovement.MovementType.IN}:
        target = _get_stock_item(cartridge_model, to_warehouse)
        target.quantity += quantity
        target.save(update_fields=['quantity'])

    if movement_type == StockMovement.MovementType.TRANSFER:
        source = _get_stock_item(cartridge_model, from_warehouse)
        target = _get_stock_item(cartridge_model, to_warehouse)
        if source.quantity < quantity:
            raise ValidationError('Insufficient stock for transfer.')
        source.quantity -= quantity
        target.quantity += quantity
        source.save(update_fields=['quantity'])
        target.save(update_fields=['quantity'])

    movement.save()
    return movement
