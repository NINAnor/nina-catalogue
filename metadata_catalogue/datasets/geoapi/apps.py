from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GeoapiConfig(AppConfig):
    name = "metadata_catalogue.datasets.geoapi"
    verbose_name = _("GeoAPI")
