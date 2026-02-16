from django.urls import path

from .views import AssetCreateView, AssetDetailView, AssetListView, AssetUpdateView, CategoryAwarePartialView

urlpatterns = [
    path('partials/category-fields/', CategoryAwarePartialView.as_view(), name='asset_category_partial'),
    path('', AssetListView.as_view(), name='asset_list'),
    path('new/', AssetCreateView.as_view(), name='asset_create'),
    path('<int:pk>/', AssetDetailView.as_view(), name='asset_detail'),
    path('<int:pk>/edit/', AssetUpdateView.as_view(), name='asset_edit'),
]
