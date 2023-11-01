from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CSWConfig(AppConfig):
    name = "metadata_catalogue.csw"
    verbose_name = _("CSW")
