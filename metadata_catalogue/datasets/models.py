import uuid

from django.contrib.gis.db import models
from django.db.models import Value
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from metadata_catalogue.core.fields import AutoOneToOneField


class Dataset(models.Model):
    class FetchType(models.IntegerChoices):
        DARWINCORE = 1, "DarwinCore Archive"

    name = models.CharField(max_length=250, verbose_name=_("Internal name"))
    uuid = models.UUIDField(default=uuid.uuid4)
    source = models.URLField(null=True, blank=True)
    fetch_url = models.URLField(verbose_name=_("URL of the resource to fetch"), null=True, blank=True)
    fetch_type = models.IntegerField(choices=FetchType.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    last_modified_at = models.DateTimeField(auto_now=True, verbose_name=_("Last modified at"))
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Owner"),
        related_name="owned_datasets",
    )
    validated_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Validated at"))
    validated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Validator"),
        related_name="validated_datasets",
    )
    fetch_success = models.BooleanField(default=False)
    fetch_message = models.TextField(null=True, blank=True)
    last_fetch_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def set_fetch_message(self, message, *args, append=False, success=None, logger_fn=None):
        text = ""
        if append and self.fetch_message:
            text = self.fetch_message

        self.fetch_message = text + message

        if success is not None:
            self.fetch_success = success
            self.last_fetch_at = now()

        if logger_fn:
            logger_fn(message)

        self.save()

    class Meta:
        verbose_name = _("Dataset")
        constraints = [
            models.UniqueConstraint(name="unique_dataset_source", fields=["fetch_url"]),
            models.UniqueConstraint(name="unique_dataset_uuid", fields=["uuid"]),
        ]


class Keyword(models.Model):
    name = models.CharField(max_length=255)
    definition = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint("name", Coalesce("definition", Value("")), name="unique_kw_name_definition")
        ]

    def __str__(self) -> str:
        return self.name


class Organization(models.Model):
    name = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_org_name",
                fields=[
                    "name",
                ],
            )
        ]


class PersonIdentifier(models.Model):
    person = models.ForeignKey("datasets.Person", on_delete=models.CASCADE)
    type = models.CharField(max_length=150)
    value = models.CharField(max_length=250)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_pers_identifier",
                fields=[
                    "person",
                    "type",
                    "value",
                ],
            )
        ]


class Person(models.Model):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    belongs_to = models.ForeignKey("datasets.Organization", on_delete=models.PROTECT, null=True, blank=True)
    position = models.CharField(max_length=250, null=True, blank=True)
    country = models.ForeignKey("countries_plus.Country", null=True, blank=True, on_delete=models.PROTECT)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    delivery_point = models.TextField(null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Coalesce("first_name", Value("")),
                Coalesce("last_name", Value("")),
                Coalesce("position", Value("")),
                Coalesce("country", Value("")),
                Coalesce("email", Value("")),
                Coalesce("belongs_to", Value(-1)),
                Coalesce("phone", Value("")),
                Coalesce("city", Value("")),
                Coalesce("delivery_point", Value("")),
                Coalesce("postal_code", Value(-1)),
                name="unique_person",
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PersonRole(models.Model):
    class RoleType(models.TextChoices):
        PROJECT_PERSONNEL = "PROJ_PERS", _("Project personnel")
        CONTACT = "CONTACT", _("Contact person")
        CREATOR = "CREATOR", _("Creator")
        PROVIDER = "PROVIDER", _("Provider")
        ASSOCIATED_PARTY = "ASSOCIATED", _("Associated party")

    person = models.ForeignKey("datasets.Person", on_delete=models.CASCADE, related_name="roles")
    metadata = models.ForeignKey("datasets.Metadata", on_delete=models.CASCADE, related_name="people")
    role = models.CharField(max_length=10)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.person} @ {self.metadata} - {self.role}"


class OrganizationRole(models.Model):
    class RoleType(models.TextChoices):
        FUNDING = "FUNDING", _("Funding")

    organization = models.ForeignKey("datasets.Organization", on_delete=models.CASCADE, related_name="roles")
    metadata = models.ForeignKey("datasets.Metadata", on_delete=models.CASCADE, related_name="organizations")
    role = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"{self.organization} @ {self.metadata} - {self.role}"


class License(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_license_name",
                fields=[
                    "name",
                ],
            ),
            models.UniqueConstraint(
                name="unique_license_url",
                fields=[
                    "url",
                ],
            ),
            models.UniqueConstraint(
                Coalesce("name", Value("")),
                Coalesce("url", Value("")),
                name="unique_license_row",
            ),
        ]


class TaxonomyType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self) -> str:
        return self.name


class Taxonomy(models.Model):
    type = models.ForeignKey("datasets.TaxonomyType", on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=250)
    common = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(name="unique_taxonomy_name_type", fields=["name", "type"])]

    def __str__(self) -> str:
        return self.name


class MethodStep(models.Model):
    order = models.IntegerField(default=0)
    description = models.TextField()


class Citation(models.Model):
    identifier = models.CharField(max_length=500, null=True, blank=True)
    text = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(name="unique_citation", fields=["identifier", "text"]),
        ]

    def __str__(self) -> str:
        return self.text


class MetadataIdentifier(models.Model):
    class Type(models.TextChoices):
        IPT = "IPT", _("IPT")
        GBIF = "GBIF", _("GBIF")

    identifier = models.CharField(max_length=500)
    metadata = models.ForeignKey("datasets.Metadata", on_delete=models.CASCADE)
    source = models.CharField(max_length=5, choices=Type.choices, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="unique_metadata_identifier", fields=["identifier", "source"]),
        ]

    def __str__(self) -> str:
        return f"{self.source} - {self.identifier}"


class Metadata(models.Model):
    dataset = AutoOneToOneField(
        "datasets.Dataset", related_name="metadata", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=500, null=True, blank=True)
    # title_alternate = models.CharField(max_length=500, null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    logo_url = models.URLField(null=True, blank=True)

    date_publication = models.DateField(null=True, blank=True)
    language = models.ForeignKey("languages_plus.Language", null=True, blank=True, on_delete=models.PROTECT)
    abstract = models.TextField(null=True, blank=True)
    keywords = models.ManyToManyField("datasets.Keyword", blank=True)
    license = models.ForeignKey("datasets.License", null=True, blank=True, on_delete=models.PROTECT)
    maintenance_update_frequency = models.TextField(
        null=True, blank=True
    )  # provide a set of choices, with default "not planned"
    maintenance_update_description = models.TextField(blank=True, null=True)

    geographic_description = models.TextField(blank=True, null=True)
    bounding_box = models.GeometryField(null=True, blank=True)

    taxonomies = models.ManyToManyField("datasets.Taxonomy", blank=True)

    citation = models.ForeignKey(
        "datasets.Citation", on_delete=models.PROTECT, null=True, blank=True, related_name="cited_by_dataset"
    )
    bibliography = models.ManyToManyField("datasets.Citation", blank=True, related_name="in_dataset_bibliography")

    formation_period_start = models.DateField(null=True, blank=True)
    formation_period_end = models.DateField(null=True, blank=True)
    formation_period_description = models.TextField(null=True, blank=True)

    project_id = models.CharField(max_length=250, blank=True, null=True)
    project_title = models.CharField(max_length=250, blank=True, null=True)
    project_abstract = models.TextField(blank=True, null=True)
    project_study_area_description = models.TextField(blank=True, null=True)
    project_design_description = models.TextField(blank=True, null=True)

    # edition = models.CharField(max_length=150, null=True, blank=True)
    # mdsource = models.CharField() # "local" or url of the resource
    # insert_date = models.DateTimeField()
    # # themes = models.ManyToManyField("datasets.Concepts", blank=True)
    # format = models.CharField() # provide choices
    # # source -- same as mdsource?
    # date = models.DateTimeField()
    # date_modified = models.DateTimeField()
    # date_revision = models.DateTimeField()
    # type = models.CharField() # TODO
    # geometry = None # TODO
    # organization = models.CharField(max_length=250)
    # security_constraints = None # TODO
    # parentidentifier = None # TODO
    # topic_category = models.ForeignKey('datasets.TopicCategory', on_delete=models.SET_NULL, null=True, blank=True)
    # geographic_description_code = models.CharField(max_length=250)
    # denominator = None # TODO
    # distance_value = None
    # distance_uom = None
    # time_begin = None
    # time_end = None
    # service_type = None
    # service_type_version = None
    # operation = None
    # coupling_type = None
    # operates_on = None

    def __str__(self) -> str:
        return self.title
