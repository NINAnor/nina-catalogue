from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from solo.admin import SingletonModelAdmin

from metadata_catalogue.datasets import models

admin.site.register(models.ServiceInfo, SingletonModelAdmin)


admin.site.register(models.Dataset)
admin.site.register(models.Person)


@admin.register(models.Metadata)
class MetadataAdmin(GISModelAdmin):
    pass
