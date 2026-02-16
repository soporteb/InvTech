from django import forms

from .models import Asset, ComputerSpecs


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'category',
            'location',
            'status',
            'observations',
            'control_patrimonial',
            'serial',
            'asset_tag_internal',
            'ownership_type',
            'provider_name',
            'responsible_employee',
        ]


class ComputerSpecsForm(forms.ModelForm):
    class Meta:
        model = ComputerSpecs
        exclude = ['asset']
