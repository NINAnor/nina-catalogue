from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict
from solo.models import SingletonModel


class CSWConfig(SingletonModel):
    language = models.CharField(max_length=7, null=True, blank=True)
    max_records = models.IntegerField(default=10)
    profiles = models.TextField(default="", blank=True)
    pretty_print = models.BooleanField(default=False)

    identification_title = models.TextField(null=True, blank=True, default="")
    identification_abstract = models.TextField(null=True, blank=True, default="")
    identification_keywords = models.TextField(null=True, blank=True, default="")
    identification_keywords_type = models.TextField(null=True, blank=True, default="")
    identification_fees = models.TextField(null=True, blank=True, default="")
    identification_accessconstraints = models.TextField(null=True, blank=True, default="")
    provider_name = models.TextField(null=True, blank=True, default="")
    provider_url = models.URLField(null=True, blank=True, default="")
    contact_name = models.TextField(null=True, blank=True, default="")
    contact_position = models.TextField(null=True, blank=True, default="")
    contact_address = models.TextField(null=True, blank=True, default="")
    contact_city = models.TextField(null=True, blank=True, default="")
    contact_stateorprovince = models.TextField(null=True, blank=True, default="")
    contact_postalcode = models.IntegerField(null=True, blank=True)
    contact_country = models.ForeignKey("countries_plus.Country", null=True, blank=True, on_delete=models.PROTECT)
    contact_phone = models.TextField(blank=True, default="")
    contact_fax = models.TextField(blank=True, default="")
    contact_email = models.TextField(null=True, blank=True, default="")
    contact_url = models.URLField(blank=True, default="")
    contact_hours = models.TextField(blank=True, default="")
    contact_instructions = models.TextField(blank=True, default="")
    contact_role = models.TextField(blank=True, default="")

    def get_config(self, url):
        metadata = model_to_dict(
            self,
            fields=[
                "identification_title",
                "identification_abstract",
                "identification_keywords",
                "identification_keywords_type",
                "identification_fees",
                "identification_accessconstraints",
                "provider_name",
                "provider_url",
                "contact_name",
                "contact_position",
                "contact_address",
                "contact_city",
                "contact_stateorprovince",
                "contact_postalcode",
                "contact_country",
                "contact_phone",
                "contact_fax",
                "contact_email",
                "contact_url",
                "contact_hours",
                "contact_instructions",
                "contact_role",
            ],
        )

        server = {
            "home": ".",
            "mimetype": "application/xml; charset=UTF-8",
            "encoding": "UTF-8",
            "language": self.language or "en-US",
            "maxrecords": str(self.max_records),
            "pretty_print": "true" if self.pretty_print else "false",
            "url": url,
        }

        if self.profiles:
            server["profiles"] = self.profiles

        return {
            "server": server,
            "metadata:main": {k: str(v) if v is not None else "" for k, v in metadata.items()},
            "repository": {
                "source": settings.CSW["repository"],
                "mappings": settings.CSW["mappings"],
            },
        }
