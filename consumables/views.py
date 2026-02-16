from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import CartridgeModelForm, StockMovementForm
from .models import CartridgeModel, StockItem, StockMovement
from .services import apply_stock_movement


class CartridgeModelListView(LoginRequiredMixin, ListView):
    model = CartridgeModel
    template_name = 'consumables/cartridge_list.html'


class CartridgeModelCreateView(LoginRequiredMixin, CreateView):
    model = CartridgeModel
    form_class = CartridgeModelForm
    template_name = 'consumables/cartridge_form.html'
    success_url = reverse_lazy('cartridge_list')


class StockView(LoginRequiredMixin, ListView):
    model = StockItem
    template_name = 'consumables/stock.html'


class StockMovementListView(LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = 'consumables/movements.html'


class StockMovementCreateView(LoginRequiredMixin, CreateView):
    template_name = 'consumables/movement_form.html'
    form_class = StockMovementForm
    success_url = reverse_lazy('stock_movements')

    def form_valid(self, form):
        apply_stock_movement(
            cartridge_model=form.cleaned_data['cartridge_model'],
            movement_type=form.cleaned_data['movement_type'],
            quantity=form.cleaned_data['quantity'],
            reason=form.cleaned_data['reason'],
            from_warehouse=form.cleaned_data['from_warehouse'],
            to_warehouse=form.cleaned_data['to_warehouse'],
            note=form.cleaned_data['note'],
        )
        messages.success(self.request, 'Stock movement registered successfully.')
        return redirect(self.success_url)
