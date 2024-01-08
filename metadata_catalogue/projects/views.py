import swapper
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

Project = swapper.load_model("projects", "Project")


class ProjectListView(ListView):
    model = Project


class ProjectDetailView(DetailView):
    model = Project


class ProjectDeleteView(DeleteView):
    model = Project

    def get_success_url(self) -> str:
        return reverse("projects-list")


class ProjectCreateView(CreateView):
    model = Project
    fields = [
        "name",
        "slug",
        "is_active",
    ]
    template_name_suffix = "_create_form"


class ProjectUpdateView(UpdateView):
    model = Project
    fields = [
        "name",
        "slug",
    ]
