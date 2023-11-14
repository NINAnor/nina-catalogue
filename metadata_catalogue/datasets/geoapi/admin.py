from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import GeoAPIConfig

admin.site.register(GeoAPIConfig, SingletonModelAdmin)
