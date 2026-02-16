from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from assets.models import Asset, AssetEvent

from .forms import LocationForm
from .models import Location


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kpis'] = {
            'assets': Asset.objects.count(),
            'assigned': Asset.objects.filter(status__name__iexact='Assigned').count(),
            'maintenance': Asset.objects.filter(status__name__iexact='Maintenance').count(),
            'locations': Location.objects.count(),
        }
        context['recent_events'] = AssetEvent.objects.select_related('asset')[:8]
        context['status_distribution'] = (
            Asset.objects.values('status__name').annotate(total=Count('id')).order_by('-total')[:5]
        )
        return context


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'locations/list.html'
    paginate_by = 20


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/form.html'
    success_url = reverse_lazy('location_list')


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'locations/form.html'
    success_url = reverse_lazy('location_list')


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = 'locations/confirm_delete.html'
    success_url = reverse_lazy('location_list')
