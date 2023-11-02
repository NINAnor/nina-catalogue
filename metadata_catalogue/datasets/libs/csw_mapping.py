from datetime import datetime

from django.apps import apps


class CSWMapping:
    def __init__(self, dataset):
        PersonRole = apps.get_model("datasets", "PersonRole")

        self.identifier = str(dataset.uuid)
        self.csw_typename = "gmd:MD_Metadata"
        self.csw_schema = "http://www.isotc211.org/2005/gmd"
        self.csw_mdsource = dataset.source
        self.csw_insert_date = datetime.strftime(dataset.created_at, "%Y-%m-%d")
        self.title = dataset.metadata.title
        self.csw_anytext = "test test test"
        self.csw_wkt_geometry = dataset.metadata.bounding_box.ewkt
        self.metadata_xml = ""
        self.language = dataset.metadata.language.iso_639_2T
        self.abstract = dataset.metadata.abstract
        self.keywords = ",".join(
            dataset.metadata.keywords.all().order_by("name").values_list("name", flat=True).distinct()
        )
        self.creator = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.CREATOR)
        self.publisher = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.PROVIDER)
        self.contributor = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.PROJECT_PERSONNEL)

    def _get_people_list_by_role(self, metadata, role):
        return " and ".join(
            [str(p) for p in metadata.people.filter(role=role).order_by("person__last_name", "person__first_name")]
        )
