from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import AssetForm
from core.models import Category

from .models import Asset
from .services import build_asset_context_for_user


class AssetListView(LoginRequiredMixin, TemplateView):
    template_name = 'assets/list.html'

    def get_filtered_queryset(self):
        queryset = Asset.objects.select_related('category', 'status', 'location', 'responsible_employee')
        q = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '').strip()
        category = self.request.GET.get('category', '').strip()
        if q:
            queryset = queryset.filter(
                Q(serial__icontains=q)
                | Q(control_patrimonial__icontains=q)
                | Q(asset_tag_internal__icontains=q)
                | Q(observations__icontains=q)
            )
        if status:
            queryset = queryset.filter(status__name__iexact=status)
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_filtered_queryset(), 12)
        page = paginator.get_page(self.request.GET.get('page', 1))
        context['page_obj'] = page
        context['is_htmx'] = self.request.headers.get('HX-Request') == 'true'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['is_htmx']:
            return render(request, 'assets/partials/asset_table.html', context)
        return self.render_to_response(context)


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = 'assets/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asset = self.object
        context['asset_context'] = build_asset_context_for_user(self.request.user, asset)
        context['tab'] = self.request.GET.get('tab', 'overview')
        return context


class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/form.html'

    def get_success_url(self):
        return reverse('asset_detail', args=[self.object.pk])


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/form.html'

    def get_success_url(self):
        return reverse('asset_detail', args=[self.object.pk])


class CategoryAwarePartialView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_name = ''
        category_id = request.GET.get('category')
        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            category_name = category.name.lower()
        template_name = 'assets/partials/category_default.html'
        if category_name in {'cpu', 'laptop', 'server'}:
            template_name = 'assets/partials/category_computer.html'
        return render(request, template_name, {'category_name': category_name})
