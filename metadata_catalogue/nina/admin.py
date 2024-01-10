from django.contrib.admin import ModelAdmin, register

from .models import Category, Department, Project, Topic


@register(Project)
class ProjectAdmin(ModelAdmin):
    search_fields = ["name", "slug", "description"]


@register(Department)
class DepartmentAdmin(ModelAdmin):
    search_fields = ["name", "slug", "description"]


@register(Category)
class CategoryAdmin(ModelAdmin):
    search_fields = ["name"]


@register(Topic)
class TopicAdmin(ModelAdmin):
    search_fields = ["name"]
