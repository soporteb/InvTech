from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied

ROLE_ADMIN = 'Admin'
ROLE_TECHNICIAN = 'IT Technician'
ROLE_VIEWER = 'Viewer'

ALL_ROLES = [ROLE_ADMIN, ROLE_TECHNICIAN, ROLE_VIEWER]


def ensure_role_groups() -> None:
    for role in ALL_ROLES:
        Group.objects.get_or_create(name=role)


def has_role(user, role_name: str) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=role_name).exists()


def is_admin(user) -> bool:
    return has_role(user, ROLE_ADMIN)


def can_view_sensitive(user) -> bool:
    return is_admin(user)


def require_role(user, *roles: str) -> None:
    if any(has_role(user, role) for role in roles):
        return
    raise PermissionDenied('User does not have required role')
