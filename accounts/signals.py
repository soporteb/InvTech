from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .roles import ensure_role_groups


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    ensure_role_groups()
