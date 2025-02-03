from django_filters import FilterSet, BooleanFilter, CharFilter
from django.forms.widgets import CheckboxInput, NullBooleanSelect
from . import models, forms


class DatasetFilter(FilterSet):
    search = CharFilter(method="filter_search", label="Full text search")
    my_datasets = BooleanFilter(
        label="My datasets", method="filter_my_datasets", widget=CheckboxInput()
    )
    public = BooleanFilter(widget=NullBooleanSelect())

    def filter_my_datasets(self, queryset, name, value):
        if value:
            return queryset.filter(owner=self.request.user)
        return queryset

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.search(value)
        return queryset

    class Meta:
        model = models.Dataset
        fields = {"public": ["exact"]}
        form = forms.DatasetFilterForm
