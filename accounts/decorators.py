from functools import wraps
from django.core.exceptions import PermissionDenied
from .roles import has_role


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if any(has_role(request.user, role) for role in roles):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied('Insufficient role')

        return _wrapped

    return decorator
