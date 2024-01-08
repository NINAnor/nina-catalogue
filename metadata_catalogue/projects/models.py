import swapper
from django.urls import reverse
from organizations.models import Organization


class BaseProject(Organization):
    class Meta:
        abstract = True


class Project(BaseProject):
    class Meta:
        swappable = swapper.swappable_setting("projects", "Project")

    def get_absolute_url(self):
        return reverse("projects-detail", kwargs={"slug": self.slug})
