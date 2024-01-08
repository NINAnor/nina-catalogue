from django.contrib.admin import ModelAdmin, register

from .models import Category, Department, Project, Topic


@register(Project)
class ProjectAdmin(ModelAdmin):
    pass


@register(Department)
class DepartmentAdmin(ModelAdmin):
    pass


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@register(Topic)
class TopicAdmin(ModelAdmin):
    pass
