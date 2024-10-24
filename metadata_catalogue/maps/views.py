from django.views.generic import DetailView, TemplateView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from .models import Portal, Visibility
from metadata_catalogue.maps import filters, tables


class ConfigJSView(DetailView):
    model = Portal
    template_name = "maps/config.js"
    content_type = "application/javascript"
    slug_field = "uuid"


class PortalPreview(TemplateView):
    """
    This is a placeholder, the frontend app will proxied
    """

    template_name = "404.html"


class PortalListPage(SingleTableMixin, FilterView):
    model = Portal
    table_class = tables.PortalTable
    filterset_class = filters.PortalFilter
    template_name = "maps/portal_list.html"

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_authenticated:
            qs = qs.filter(visibility=Visibility.PUBLIC)

        return qs
