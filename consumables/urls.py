from django.urls import path

from .views import (
    CartridgeModelCreateView,
    CartridgeModelListView,
    StockMovementCreateView,
    StockMovementListView,
    StockView,
)

urlpatterns = [
    path('cartridges/', CartridgeModelListView.as_view(), name='cartridge_list'),
    path('cartridges/new/', CartridgeModelCreateView.as_view(), name='cartridge_create'),
    path('stock/', StockView.as_view(), name='stock_view'),
    path('movements/', StockMovementListView.as_view(), name='stock_movements'),
    path('movements/new/', StockMovementCreateView.as_view(), name='stock_movement_create'),
]
