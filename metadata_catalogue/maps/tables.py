import django_tables2 as tables
from . import models
from django_tables2.utils import A


class PortalTable(tables.Table):
    title = tables.LinkColumn("maps:portal-preview", kwargs={"slug": A("uuid")})

    class Meta:
        model = models.Portal
        fields = (
            "title",
            "uuid",
            "visibility",
            "owner",
        )
        template_name = "django_tables2/bootstrap.html"
