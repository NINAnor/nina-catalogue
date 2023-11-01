from django.contrib import admin
from solo.admin import SingletonModelAdmin

from metadata_catalogue.csw.models import CSWConfig

admin.site.register(CSWConfig, SingletonModelAdmin)
