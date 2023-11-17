from django.apps import apps
from django.conf import settings
from django.db import models
from solo.models import SingletonModel

from ..libs.utils import safe_get


class CSWConfig(SingletonModel):
    max_records = models.IntegerField(default=10)
    profiles = models.TextField(default="apiso", blank=True)
    pretty_print = models.BooleanField(default=False)

    def get_config(self, url=""):
        ServiceInfo = apps.get_model("datasets", "ServiceInfo")

        info = ServiceInfo.get_solo()

        server = {
            "home": ".",
            "mimetype": "application/xml; charset=UTF-8",
            "encoding": "UTF-8",
            "language": info.language or "en-US",
            "maxrecords": str(self.max_records),
            "pretty_print": "true" if self.pretty_print else "false",
            "url": url,
        }

        if self.profiles:
            server["profiles"] = self.profiles

        return {
            "server": server,
            "metadata:main": {
                "identification_title": info.identification_title,
                "identification_abstract": info.identification_abstract,
                "identification_keywords": info.identification_keywords,
                "identification_keywords_type": info.identification_keywords_type,
                "identification_fees": info.identification_fees,
                "identification_accessconstraints": info.identification_accessconstraints,
                "provider_name": str(info.provider),
                "provider_url": "",
                "contact_name": str(info.contact),
                "contact_position": safe_get(info.contact, "position"),
                "contact_address": safe_get(info.contact, "delivery_point"),
                "contact_city": safe_get(info.contact, "city"),
                "contact_stateorprovince": str(safe_get(info.contact, "country")),
                "contact_postalcode": safe_get(info.contact, "postal_code"),
                "contact_country": str(safe_get(info.contact, "country")),
                "contact_phone": safe_get(info.contact, "phone"),
                "contact_fax": safe_get(info.contact, "phone"),
                "contact_email": safe_get(info.contact, "email"),
                "contact_url": "",
                "contact_hours": info.contact_hours or "",
                "contact_instructions": info.contact_instructions or "",
                "contact_role": "pointOfContact",
            },
            "repository": {
                "source": settings.CSW["repository"],
                "mappings": settings.CSW["mappings"],
            },
        }
