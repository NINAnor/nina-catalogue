from typing import Any

from django.views.generic import DetailView, ListView
from django_filters.views import FilterView

from metadata_catalogue.projects import views

from .filters import ProjectFilter
from .models import Department, Project


class ProjectListView(FilterView):
    model = Project
    paginate_by = 20
    filterset_class = ProjectFilter


class ProjectUpdateView(views.ProjectUpdateView):
    fields = ["description", "tags", "topics"]


class ProjectDetailView(views.ProjectDetailView):
    pass


class DepartmentListView(ListView):
    paginate_by = 20
    model = Department


class DepartmentDetailView(DetailView):
    model = Department
