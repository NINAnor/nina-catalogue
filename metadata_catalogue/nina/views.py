from typing import Any

from django.views.generic import DetailView, ListView, UpdateView
from django_filters.views import FilterView
from rules.contrib.views import PermissionRequiredMixin

from metadata_catalogue.projects import views

from .filters import ProjectFilter
from .forms import ProjectEditForm
from .models import Department, Project


class ProjectListView(FilterView):
    model = Project
    paginate_by = 20
    filterset_class = ProjectFilter


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = ProjectEditForm
    model = Project
    permission_required = "nina.project_edit"


class ProjectDetailView(views.ProjectDetailView):
    pass


class DepartmentListView(ListView):
    paginate_by = 20
    model = Department


class DepartmentDetailView(DetailView):
    model = Department
