from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DatasetsConfig(AppConfig):
    name = "metadata_catalogue.datasets"
    verbose_name = _("Datasets")

    def ready(self):
        try:
            import metadata_catalogue.datasets.signals  # noqa: F401
        except ImportError:
            pass
