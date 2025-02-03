from django_filters import rest_framework as filters

from .models import PortalMap, Portal


class PortalMapFilter(filters.FilterSet):
    portal = filters.CharFilter(method="portal_filter")

    class Meta:
        model = PortalMap
        fields = ["portal"]

    def portal_filter(self, queryset, name, value):
        return queryset.filter(portal__uuid=value)


class PortalFilter(filters.FilterSet):
    class Meta:
        model = Portal
        fields = ["visibility"]
