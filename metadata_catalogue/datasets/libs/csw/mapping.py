import json
from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.urls import reverse_lazy


class CSWMapping:
    def __init__(self, dataset, base_url=""):
        PersonRole = apps.get_model("datasets", "PersonRole")
        self.identifier = str(dataset.uuid)
        self.csw_typename = "gmd:MD_Metadata"
        self.csw_schema = "http://www.isotc211.org/2005/gmd"
        self.csw_mdsource = dataset.source
        self.csw_insert_date = datetime.strftime(dataset.created_at, "%Y-%m-%d")
        self.title = dataset.metadata.title
        self.csw_wkt_geometry = dataset.metadata.bounding_box.ewkt
        self.language = dataset.metadata.language.iso_639_2T
        self.abstract = dataset.metadata.abstract
        self.format = "OGCFeat"
        self.source = settings.BASE_SCHEMA_URL + reverse_lazy(
            "geoapi:collection-detail", kwargs={"collection_id": str(dataset.uuid)}
        )
        self.type = "service"
        self.keywords = ",".join(
            dataset.metadata.keywords.all().order_by("name").values_list("name", flat=True).distinct()
        )
        self.creator = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.CREATOR)
        self.publisher = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.PROVIDER)
        self.contributor = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.PROJECT_PERSONNEL)
        self.metadata_xml = dataset.metadata.xml
        self.csw_anytext = dataset.metadata.fts
        self.links = json.dumps(
            [
                {
                    "url": settings.BASE_SCHEMA_URL
                    + reverse_lazy("geoapi:collection-detail", kwargs={"collection_id": str(dataset.uuid)}),
                    "protocol": "OGCFeat",
                    "name": "OGC API Feature",
                    "description": "OGC REST API to the resource",
                }
            ]
        )

    def _get_people_list_by_role(self, metadata, role):
        return " and ".join(
            [str(p) for p in metadata.people.filter(role=role).order_by("person__last_name", "person__first_name")]
        )
