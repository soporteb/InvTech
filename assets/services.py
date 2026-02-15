from accounts.roles import can_view_sensitive


def build_asset_context_for_user(user, asset):
    context = {
        'asset_id': asset.id,
        'padlock': 'Yes' if asset.has_padlock else 'No',
        'license': 'Yes' if asset.has_license else 'No',
    }
    if can_view_sensitive(user) and hasattr(asset, 'sensitive_data'):
        context['sensitive'] = {
            'cpu_padlock_key': asset.sensitive_data.cpu_padlock_key,
            'license_key': asset.sensitive_data.license_key,
            'admin_secret_note': asset.sensitive_data.admin_secret_note,
        }
    return context
