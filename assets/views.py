from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from assignments.forms import ReassignForm, ReturnAssetForm
from assignments.services import reassign_asset, return_asset
from core.models import Category, Status

from .forms import AssetForm, AssetOperationForm
from .models import Asset, AssetEvent, AssetOperation
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
        context['reassign_form'] = ReassignForm()
        context['return_form'] = ReturnAssetForm()
        context['operation_form'] = AssetOperationForm()
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


class AssetReassignView(LoginRequiredMixin, View):
    def post(self, request, pk):
        asset = get_object_or_404(Asset, pk=pk)
        form = ReassignForm(request.POST)
        if form.is_valid():
            reassign_asset(
                asset=asset,
                new_employee=form.cleaned_data['employee'],
                reason=form.cleaned_data['reason'],
                created_by=request.user,
                note=form.cleaned_data['note'],
            )
            messages.success(request, 'Asset reassigned successfully.')
        else:
            messages.error(request, 'Failed to reassign asset. Check required fields.')
        return redirect('asset_detail', pk=pk)


class AssetReturnView(LoginRequiredMixin, View):
    def post(self, request, pk):
        asset = get_object_or_404(Asset, pk=pk)
        form = ReturnAssetForm(request.POST)
        if form.is_valid():
            return_asset(
                asset=asset,
                reason=form.cleaned_data['reason'],
                created_by=request.user,
                note=form.cleaned_data['note'],
            )
            messages.success(request, 'Asset returned/unassigned successfully.')
        else:
            messages.error(request, 'Return action failed.')
        return redirect('asset_detail', pk=pk)


class AssetOperationCreateView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request, pk):
        asset = get_object_or_404(Asset, pk=pk)
        form = AssetOperationForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Operation data is invalid.')
            return redirect('asset_detail', pk=pk)

        operation = form.save(commit=False)
        operation.asset = asset
        operation.created_by = request.user
        operation.save()

        summary = f'Asset operation: {operation.operation_type}'
        event_type = AssetEvent.EventType.UPDATED
        if operation.operation_type == AssetOperation.OperationType.MAINTENANCE:
            event_type = AssetEvent.EventType.MAINTENANCE
        AssetEvent.objects.create(
            asset=asset,
            event_type=event_type,
            actor=request.user,
            summary=summary,
            details_json={'justification': operation.justification},
        )

        status_name = {
            AssetOperation.OperationType.MAINTENANCE: 'Maintenance',
            AssetOperation.OperationType.REPLACEMENT: 'Available',
            AssetOperation.OperationType.DECOMMISSION: 'Decommissioned',
        }[operation.operation_type]
        status = Status.objects.filter(name__iexact=status_name).first()
        if status:
            asset.status = status
            asset.save(update_fields=['status', 'updated_at'])

        messages.success(request, 'Asset operation recorded.')
        return redirect('asset_detail', pk=pk)
