from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import Model
from django.db.models.query import QuerySet

from metadata_catalogue.projects import views


class ProjectListView(views.ProjectListView):
    paginate_by = 20


class ProjectUpdateView(views.ProjectUpdateView):
    fields = ["description", "tags", "topics"]


class ProjectDetailView(views.ProjectDetailView):
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(extid=self.kwargs.get("extid"))
        except ObjectDoesNotExist:
            return super().get_object(queryset)
