from pathlib import Path

from django.apps import apps
from django.db import models
from pygeoapi.openapi import get_oas
from solo.models import SingletonModel

from ..libs.utils import safe_get


class GeoAPIConfig(SingletonModel):
    max_records = models.IntegerField(default=10)
    pretty_print = models.BooleanField(default=False)
    map_url = models.URLField(default="https://tile.openstreetmap.org/{z}/{x}/{y}.png")
    map_attribution = models.TextField(
        default='&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    )

    def get_config(self, url=""):
        ServiceInfo = apps.get_model("datasets", "ServiceInfo")
        Dataset = apps.get_model("datasets", "Dataset")
        info = ServiceInfo.objects.select_related("contact", "license", "provider").get()

        resources = {
            id: value for id, value in Dataset.objects.select_related("metadata").all().as_geoapi_resource(url)
        }

        conf = {
            "server": {
                "mimetype": "application/xml; charset=UTF-8",
                "encoding": "utf-8",
                "language": info.language or "en-US",
                "limit": str(self.max_records),
                "pretty_print": self.pretty_print,
                "url": url + "/geoapi",
                "templates": {"static": str(Path(__name__).parent / "statics" / "geoapi")},
                "map": {
                    "url": self.map_url,
                    "attribute": self.map_attribution,
                },
            },
            "logging": {
                "level": "DEBUG",
            },
            "metadata": {
                "identification": {
                    "title": info.identification_title,
                    "description": info.identification_abstract,
                    "keywords": info.identification_keywords.split(",") if info.identification_keywords else "",
                    "keywords_type": "theme",
                    "terms_of_service": info.identification_accessconstraints,
                    "url": "",
                },
                "license": {
                    "name": info.license.name if info.license else "",
                    "url": info.license.url if info.license else "",
                },
                "provider": {
                    "name": str(info.provider),
                    "url": "",
                },
                "contact": {
                    "name": str(info.contact),
                    "position": safe_get(info.contact, "position"),
                    "address": safe_get(info.contact, "delivery_point"),
                    "city": safe_get(info.contact, "city"),
                    "stateorprovince": safe_get(info.contact, "country"),
                    "postalcode": safe_get(info.contact, "postal_code"),
                    "country": str(safe_get(info.contact, "country")),
                    "phone": safe_get(info.contact, "phone"),
                    "fax": safe_get(info.contact, "phone"),
                    "email": safe_get(info.contact, "email"),
                    "url": "",
                    "hours": info.contact_hours or "",
                    "instructions": info.contact_instructions or "",
                    "role": "pointOfContact",
                },
            },
            "resources": resources,
        }

        print(conf["metadata"])

        openapi = get_oas(conf)
        return conf, openapi
