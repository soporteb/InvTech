from django.urls import path

from .views import LocationCreateView, LocationDeleteView, LocationListView, LocationUpdateView

urlpatterns = [
    path('', LocationListView.as_view(), name='location_list'),
    path('new/', LocationCreateView.as_view(), name='location_create'),
    path('<int:pk>/edit/', LocationUpdateView.as_view(), name='location_edit'),
    path('<int:pk>/delete/', LocationDeleteView.as_view(), name='location_delete'),
]
