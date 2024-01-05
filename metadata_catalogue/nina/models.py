from django.db import models
from taggit.managers import TaggableManager

from metadata_catalogue.projects.models import BaseProject


class Project(BaseProject):
    code = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.PositiveBigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey("nina.Category", null=True, blank=True, on_delete=models.SET_NULL)
    topics = models.ManyToManyField("nina.Topic", blank=True)

    tags = TaggableManager()

    class Meta:
        constraints = [models.UniqueConstraint("code", name="unique project code")]


class Topic(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        constraints = [models.UniqueConstraint("name", name="unique topic name")]


class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        constraints = [models.UniqueConstraint("name", name="unique category name")]
