from django.db import models
from django_extensions.db.fields import AutoSlugField
from taggit.managers import TaggableManager

from metadata_catalogue.projects.models import BaseProject, BaseProjectMembership

from .conf import settings


class Project(BaseProject):
    id = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey("nina.Category", null=True, blank=True, on_delete=models.SET_NULL)
    topics = models.ManyToManyField("nina.Topic", blank=True)
    departments = models.ManyToManyField("nina.Department", blank=True, related_name="projects")
    customer = models.ForeignKey("datasets.Organization", blank=True, on_delete=models.SET_NULL, null=True)

    tags = TaggableManager()

    def __str__(self) -> str:
        return self.name


class ProjectMembership(BaseProjectMembership):
    pass


class Topic(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        constraints = [models.UniqueConstraint("name", name="unique topic name")]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        constraints = [models.UniqueConstraint("name", name="unique category name")]

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from=["name"])
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, through="nina.DepartmentMembership", related_name="members"
    )

    def __str__(self) -> str:
        return self.name


class DepartmentMembership(models.Model):
    department = models.ForeignKey("nina.Department", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
