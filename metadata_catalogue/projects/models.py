import swapper
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from .conf import settings


class BaseProject(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from=["name"])
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, through=swapper.get_model_name("projects", "ProjectMembership")
    )

    class Meta:
        abstract = True


class BaseProjectMembership(models.Model):
    project = models.ForeignKey(swapper.get_model_name("projects", "Project"), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects_membership")

    class Meta:
        abstract = True


class Project(BaseProject):
    class Meta:
        swappable = swapper.swappable_setting("projects", "Project")

    def get_absolute_url(self):
        return reverse("projects-detail", kwargs={"slug": self.slug})


class ProjectMembership(BaseProjectMembership):
    class Meta:
        swappable = swapper.swappable_setting("projects", "ProjectMembership")
        constraints = [models.UniqueConstraint(["project", "user"], name="unique user per project")]
