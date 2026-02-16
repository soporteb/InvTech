from django import forms

from .models import CartridgeModel, StockMovement, Warehouse


class CartridgeModelForm(forms.ModelForm):
    class Meta:
        model = CartridgeModel
        fields = ['brand', 'model', 'description']


class StockMovementForm(forms.Form):
    cartridge_model = forms.ModelChoiceField(queryset=CartridgeModel.objects.all().order_by('brand', 'model'))
    movement_type = forms.ChoiceField(choices=StockMovement.MovementType.choices)
    quantity = forms.IntegerField(min_value=1)
    from_warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all().order_by('name'), required=False)
    to_warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all().order_by('name'), required=False)
    reason = forms.CharField(max_length=255)
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
