from django.db import transaction
from django.utils import timezone

from assets.models import AssetEvent

from .models import AssetAssignment


@transaction.atomic
def reassign_asset(*, asset, new_employee, reason, created_by=None, note=''):
    today = timezone.localdate()
    current = (
        AssetAssignment.objects.select_for_update()
        .filter(asset=asset, end_date__isnull=True)
        .order_by('-start_date', '-created_at')
        .first()
    )
    if current:
        current.end_date = today
        current.note = (current.note or '') + ('\n' if current.note and note else '') + (note or '')
        current.save(update_fields=['end_date', 'note'])

    new_assignment = AssetAssignment.objects.create(
        asset=asset,
        employee=new_employee,
        start_date=today,
        reason=reason,
        note=note,
        created_by=created_by,
    )

    asset.responsible_employee = new_employee
    asset.save(update_fields=['responsible_employee', 'updated_at'])

    AssetEvent.objects.create(
        asset=asset,
        event_type=AssetEvent.EventType.ASSIGNED,
        actor=created_by,
        summary='Asset reassigned',
        details_json={'employee_id': new_employee.id, 'reason_id': reason.id},
    )
    return new_assignment


@transaction.atomic
def return_asset(*, asset, reason, created_by=None, note=''):
    today = timezone.localdate()
    current = (
        AssetAssignment.objects.select_for_update()
        .filter(asset=asset, end_date__isnull=True)
        .order_by('-start_date', '-created_at')
        .first()
    )
    if current:
        current.end_date = today
        current.note = (current.note or '') + ('\n' if current.note and note else '') + (note or '')
        current.reason = reason
        current.save(update_fields=['end_date', 'note', 'reason'])

    asset.responsible_employee = None
    asset.save(update_fields=['responsible_employee', 'updated_at'])

    AssetEvent.objects.create(
        asset=asset,
        event_type=AssetEvent.EventType.UNASSIGNED,
        actor=created_by,
        summary='Asset returned/unassigned',
        details_json={'reason_id': reason.id},
    )
