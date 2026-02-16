from django.contrib import admin
from django.urls import include, path

from core.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', DashboardView.as_view(), name='dashboard'),
    path('assets/', include('assets.urls')),
    path('employees/', include('employees.urls')),
    path('locations/', include('core.urls')),
    path('consumables/', include('consumables.urls')),
]
