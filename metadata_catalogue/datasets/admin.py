from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from solo.admin import SingletonModelAdmin

from metadata_catalogue.datasets import models

admin.site.register(models.ServiceInfo, SingletonModelAdmin)


@admin.register(models.Dataset)
class DatasetAdmin(admin.ModelAdmin):
    search_fields = [
        "id",
        "uuid",
        "name",
        "fetch_url",
    ]

    list_display = [
        "id",
        "name",
        "uuid",
        "source",
        "fetch_type",
        "fetch_success",
        "last_fetch_at",
    ]

    list_filter = [
        "fetch_type",
        "fetch_success",
    ]


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    search_fields = [
        "id",
        "dataset__uuid",
        "dataset__name",
        "gdal_vrt_definition",
    ]

    list_display = [
        "dataset_id",
        "dataset",
        "valid",
        "gdal_vrt_definition",
    ]

    list_filter = ["valid"]


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = [
        "id",
        "first_name",
        "last_name",
        "email",
    ]

    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "country",
        "belongs_to",
        "position",
    ]


@admin.register(models.Metadata)
class MetadataAdmin(GISModelAdmin):
    search_fields = [
        "title",
        "abstract",
        "dataset__uuid",
        "dataset__title",
    ]

    list_display = [
        "dataset_id",
        "title",
        "abstract",
    ]


@admin.register(models.PersonRole)
class PersonRoleAdmin(admin.ModelAdmin):
    search_fields = [
        "role",
        "person__first_name",
        "person__last_name",
        "person__email",
    ]

    list_display = ["person", "metadata", "role"]

    list_filter = [
        "role",
    ]


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]

    list_display = [
        "name",
        "url",
    ]


@admin.register(models.PersonIdentifier)
class PersonIdentifierAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OrganizationRole)
class OrganizationRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TaxonomyType)
class TaxonomyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MetadataIdentifier)
class MetadataIdentifierAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Citation)
class CitationAdmin(admin.ModelAdmin):
    pass
