from datetime import datetime

from django.apps import apps
from pygeometa.schemas.iso19139 import ISO19139OutputSchema

iso_os = ISO19139OutputSchema()


def safe_get(element, attribute):
    if element:
        if (v := element.__getattribute__(attribute)) is not None:
            return v
    return ""


class CSWMapping:
    def __init__(self, dataset):
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
        self.keywords = ",".join(
            dataset.metadata.keywords.all().order_by("name").values_list("name", flat=True).distinct()
        )
        self.creator = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.CREATOR)
        self.publisher = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.PROVIDER)
        self.contributor = self._get_people_list_by_role(dataset.metadata, PersonRole.RoleType.PROJECT_PERSONNEL)

        self.csw_anytext = " ".join(
            [
                dataset.metadata.title,
                dataset.metadata.abstract,
                self.keywords,
                self.creator,
                self.publisher,
                dataset.source,
                self.identifier,
            ]
        )
        self._as_iso_xml(dataset)

    def _get_people_list_by_role(self, metadata, role):
        return " and ".join(
            [str(p) for p in metadata.people.filter(role=role).order_by("person__last_name", "person__first_name")]
        )

    def _mfc_person(self, person):
        """
        Serialize a Person using MFC
        """
        return {
            "organization": safe_get(person.belongs_to, "name"),
            "url": "",
            "individualname": str(person),
            "positionname": safe_get(person, "position"),
            "phone": safe_get(person, "phone"),
            "fax": safe_get(person, "phone"),
            "address": safe_get(person, "delivery_point"),
            "city": safe_get(person, "city"),
            "administrativearea": "",
            "postalcode": safe_get(person, "postal_code"),
            "country": safe_get(person.country, "name"),
        }

    def _mfc_keywords(self, metadata):
        groups = {}
        for k in metadata.keywords.all():
            group = str(k.definition or "default").replace(r"https?://", "")
            if not group in groups:
                groups[group] = {
                    "keywords": [],
                    "keywords_type": "theme",
                }

                if group != "default":
                    groups[group]["vocabulary"] = {"name": k.description, "url": k.definition}

            groups[group]["keywords"].append(k.name)

        return groups

    def _as_iso_xml(self, dataset):
        """
        Represents the dataset using MFC (Metadata Control File) dictionary of pygeometa
        Reference: https://geopython.github.io/pygeometa/reference/mcf/
        """
        PersonRole = apps.get_model("datasets", "PersonRole")
        contact = dataset.metadata.people.filter(role=PersonRole.RoleType.CONTACT).first().person
        provider = dataset.metadata.people.filter(role=PersonRole.RoleType.PROVIDER).first().person

        mfc = {
            "version": "1.0",
            "metadata": {
                "identifier": self.identifier,
                "language": dataset.metadata.language.iso_639_1,
                "charset": "utf8",
                "hierarchylevel": "dataset",
                "datestamp": dataset.created_at,
            },
            "spatial": {"datatype": "vector", "geomtype": "point"},
            "identification": {
                "title": dataset.metadata.title,
                "abstract": dataset.metadata.abstract,
                "topiccategory": "",
                "fees": "None",
                "accessconstraints": "None",
                "rights": "",
                "url": dataset.source,
                "status": "completed",
                "maintenancefrequency": "unknown",
                "dates": {
                    "creation": dataset.created_at,
                },
                "extents": {
                    "spatial": [
                        {
                            "crs": dataset.metadata.bounding_box.srid,
                            "bbox": dataset.metadata.bounding_box.extent,
                            "description": dataset.metadata.geographic_description,
                        }
                    ]
                },
                "keywords": self._mfc_keywords(dataset.metadata),
                "license": {
                    "name": dataset.metadata.license.name,
                    "url": dataset.metadata.license.url,
                },
            },
            "content_info": {
                "type": "feature_catalogue",
            },
            "contact": {
                "pointOfContact": self._mfc_person(contact),
                "distributor": self._mfc_person(provider),
            },
            "distribution": {
                "dwca": {
                    "url": dataset.fetch_url,
                    "type": "download",
                    "name": "DarwinCore Archive",
                    "description": "",
                    "function": "download",
                }
            },
        }

        self.metadata_xml = iso_os.write(mfc)
