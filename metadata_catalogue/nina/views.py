from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, ListView

from metadata_catalogue.projects import views

from .models import Department


class ProjectListView(views.ProjectListView):
    paginate_by = 20


class ProjectUpdateView(views.ProjectUpdateView):
    fields = ["description", "tags", "topics"]


class ProjectDetailView(views.ProjectDetailView):
    pass


class DepartmentListView(ListView):
    paginate_by = 20
    model = Department


class DepartmentDetailView(DetailView):
    model = Department
