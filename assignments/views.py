from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import AssetAssignment, AssignmentReason


class AssignmentListView(LoginRequiredMixin, ListView):
    model = AssetAssignment
    template_name = 'assignments/list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = (
            AssetAssignment.objects.select_related('asset', 'employee', 'reason', 'asset__location', 'asset__category')
            .order_by('-start_date', '-created_at')
        )
        q = self.request.GET.get('q', '').strip()
        state = self.request.GET.get('state', '').strip().lower()
        if q:
            queryset = queryset.filter(
                Q(employee__names__icontains=q)
                | Q(employee__dni__icontains=q)
                | Q(asset__serial__icontains=q)
                | Q(asset__control_patrimonial__icontains=q)
                | Q(asset__asset_tag_internal__icontains=q)
            )
        if state == 'active':
            queryset = queryset.filter(end_date__isnull=True)
        elif state == 'closed':
            queryset = queryset.filter(end_date__isnull=False)
        return queryset


class AssignmentReasonCreateView(LoginRequiredMixin, CreateView):
    model = AssignmentReason
    fields = ['name']
    template_name = 'assignments/reason_form.html'
    success_url = reverse_lazy('assignment_list')
