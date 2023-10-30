from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Dataset(models.Model):
    class FetchType(models.IntegerChoices):
        DARWINCORE = 1, "DarwinCORE"

    name = models.CharField(max_length=250, verbose_name=_("Internal name"))
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Dataset")


class Keyword(models.Model):
    name = models.CharField(max_length=255)
    definition = models.URLField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(name="unique_kw_name_definition", fields=["name", "definition"])]

    def __str__(self) -> str:
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=250)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_person", fields=["first_name", "last_name", "position", "country", "email", "belongs_to"]
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PersonRole(models.Model):
    class RoleType(models.TextChoices):
        PROJECT_PERSONNEL = "PROJ_PERS", _("Project personnel")
        CONTACT = "CONTACT", _("Contact person")
        CREATOR = "CREATOR", _("CREATOR")
        PROVIDER = "PROVIDER", _("PROVIDER")

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
        ]


class TaxonomyType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self) -> str:
        return self.name


class Taxonomy(models.Model):
    type = models.ForeignKey("datasets.TaxonomyType", on_delete=models.PROTECT)
    name = models.CharField(max_length=150)

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
    id = models.CharField(max_length=500, primary_key=True)
    metadata = models.ForeignKey("datasets.Metadata", on_delete=models.CASCADE)


class Metadata(models.Model):
    dataset = models.OneToOneField(
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
    maintenance_update_description = models.TextField(blank=True)

    geographic_description = models.TextField(blank=True)
    bounding_box = models.GeometryField(null=True, blank=True)

    taxonomies = models.ManyToManyField("datasets.Taxonomy", blank=True)

    citation = models.ForeignKey(
        "datasets.Citation", on_delete=models.PROTECT, null=True, blank=True, related_name="cited_by_dataset"
    )
    bibliography = models.ManyToManyField("datasets.Citation", blank=True, related_name="in_dataset_bibliography")

    formation_period_start = models.DateField(null=True, blank=True)
    formation_period_end = models.DateField(null=True, blank=True)

    project_id = models.CharField(max_length=250, blank=True, null=True)
    project_title = models.CharField(max_length=250, blank=True, null=True)
    project_abstract = models.TextField(blank=True)
    project_study_area_description = models.TextField(blank=True)
    project_design_description = models.TextField(blank=True)

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
