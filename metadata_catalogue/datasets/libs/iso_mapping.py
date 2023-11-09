from django.apps import apps
from pycsw.core.util import get_anytext
from pygeometa.schemas.iso19139 import ISO19139OutputSchema

from .utils import safe_get

iso_os = ISO19139OutputSchema()


class ISOMapping:
    def __init__(self, dataset):
        PersonRole = apps.get_model("datasets", "PersonRole")
        contact = dataset.metadata.people.filter(role=PersonRole.RoleType.CONTACT).first().person
        provider = dataset.metadata.people.filter(role=PersonRole.RoleType.PROVIDER).first().person

        self.data = {
            "version": "1.0",
            "metadata": {
                "identifier": dataset.uuid,
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
                "keywords": self._keywords(dataset.metadata),
                "license": {
                    "name": dataset.metadata.license.name,
                    "url": dataset.metadata.license.url,
                },
            },
            "content_info": {
                "type": "feature_catalogue",
            },
            "contact": {
                "pointOfContact": self._person(contact),
                "distributor": self._person(provider),
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

    def to_xml_string(self):
        return iso_os.write(self.data)

    @classmethod
    def to_text(cls, text):
        return get_anytext(text)

    def _person(self, person):
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

    def _keywords(self, metadata):
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
