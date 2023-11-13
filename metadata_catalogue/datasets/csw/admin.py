from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import CSWConfig

admin.site.register(CSWConfig, SingletonModelAdmin)
