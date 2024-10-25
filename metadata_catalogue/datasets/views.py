from django.http import HttpResponse, HttpResponseNotFound
from .models import Dataset, Metadata
from . import tables, forms, filters
from django.views.generic import CreateView, DetailView, UpdateView
from typing import Any
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.aggregates import ArrayAgg
from django.urls import reverse


def get_dataset_vrt_view(request, dataset_uuid):
    try:
        dataset = Dataset.objects.select_related("content").get(uuid=dataset_uuid)
        return HttpResponse(dataset.content.gdal_vrt_definition, content_type="text")
    except Dataset.DoesNotExist:
        return HttpResponseNotFound()


class DatasetsListPage(SingleTableMixin, FilterView):
    model = Dataset
    table_class = tables.DatasetTable
    filterset_class = filters.DatasetFilter
    template_name = "datasets/dataset_list.html"

    def get_queryset(self):
        qs = super().get_queryset().order_by("created_at")

        if not self.request.user.is_authenticated:
            qs = qs.filter(public=True)

        return qs


class DatasetCreatePage(LoginRequiredMixin, CreateView):
    form_class = forms.DatasetCreateForm
    model = Dataset

    def get_form_kwargs(self) -> dict[str, Any]:
        ctx = super().get_form_kwargs()
        ctx["user"] = self.request.user
        return ctx


class DatasetDetailPage(DetailView):
    model = Dataset
    slug_field = "uuid"

    def get_queryset(self):
        qs = super().get_queryset().select_related("metadata")

        if not self.request.user.is_authenticated:
            qs = qs.filter(public=True)

        return qs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        ctx["people_table"] = tables.RolesTable(
            self.object.metadata.people.values(
                "person__last_name", "person__first_name"
            )
            .annotate(
                role=ArrayAgg(
                    "role",
                )
            )
            .order_by("person__last_name", "person__first_name"),
            prefix="people-",
        )

        return ctx


class DatasetEditPage(UpdateView):
    model = Metadata
    slug_field = "dataset__uuid"
    form_class = forms.DatasetMetadataEditForm
    template_name = "datasets/dataset_edit.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related("dataset")

        if not self.request.user.is_authenticated:
            qs = qs.filter(dataset__public=True)
        else:
            qs = qs.filter(dataset__owner=self.request.user)

        return qs

    def get_success_url(self) -> str:
        return reverse("dataset-detail", kwargs=dict(slug=self.object.dataset.uuid))
