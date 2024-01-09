from django.db import models
from organizations.models import Organization
from taggit.managers import TaggableManager

from metadata_catalogue.projects.models import BaseProject


class Project(BaseProject):
    extid = models.CharField(max_length=100)
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

    class Meta:
        constraints = [models.UniqueConstraint("extid", name="unique project code")]

    def __str__(self) -> str:
        return self.name


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


class Department(Organization):
    extid = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint("extid", name="unique departemt extid")]

    def __str__(self) -> str:
        return self.name
