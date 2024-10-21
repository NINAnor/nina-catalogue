import django_tables2 as tables
from . import models
from django_tables2.utils import A


class DatasetTable(tables.Table):
    name = tables.LinkColumn("dataset-detail", kwargs={"slug": A("uuid")})
    metadata__date_publication = tables.DateColumn(format="d/m/Y")

    class Meta:
        model = models.Dataset
        fields = (
            "name",
            "metadata__language",
            "metadata__license",
            "metadata__date_publication",
            "public",
            "owner",
        )
        template_name = "django_tables2/bootstrap.html"


class RolesTable(tables.Table):
    class Meta:
        model = models.PersonRole
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "person",
            "role",
        )
