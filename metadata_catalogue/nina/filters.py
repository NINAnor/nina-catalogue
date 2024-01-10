import django_filters
from taggit.forms import TagField

from .forms import ProjectSearchForm
from .models import Project


class TagFilter(django_filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "in")
        super().__init__(*args, **kwargs)


class ProjectFilter(django_filters.FilterSet):
    tags = TagFilter(field_name="tags__name")

    class Meta:
        model = Project
        form = ProjectSearchForm
        fields = ["status", "topics", "category", "departments", "customer"]
