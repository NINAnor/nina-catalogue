from django.contrib.admin import ModelAdmin, site

from .conf import settings
from .models import Project, ProjectMembership


class ProjectAdmin(ModelAdmin):
    pass


class ProjectMembershipAdmin(ModelAdmin):
    pass


if not settings.PROJECTS_PROJECT_MODEL or settings.PROJECTS_PROJECT_MODEL == "projects.Project":
    site.register(Project, ProjectAdmin)

if (
    not settings.PROJECTS_PROJECTMEMBERSHIP_MODEL
    or settings.PROJECTS_PROJECTMEMBERSHIP_MODEL == "projects.ProjectMembership"
):
    site.register(ProjectMembershipAdmin, ProjectMembershipAdmin)
