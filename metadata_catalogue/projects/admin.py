from django.contrib.admin import ModelAdmin, site

from .conf import settings
from .models import Project


class ProjectAdmin(ModelAdmin):
    pass


if not settings.PROJECTS_PROJECT_MODEL or settings.PROJECTS_PROJECT_MODEL == "projects.Project":
    site.register(Project, ProjectAdmin)
