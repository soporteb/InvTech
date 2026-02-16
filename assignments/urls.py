from django.urls import path

from .views import AssignmentListView, AssignmentReasonCreateView

urlpatterns = [
    path('', AssignmentListView.as_view(), name='assignment_list'),
    path('reasons/new/', AssignmentReasonCreateView.as_view(), name='assignment_reason_create'),
]
