from django.urls import path

from .views import ProjectCreateView, ProjectDeleteView, ProjectDetailView, ProjectListView, ProjectUpdateView

urlpatterns = [
    path("", ProjectListView.as_view(), name="projects-list"),
    path("create/", ProjectCreateView.as_view(), name="projects-create"),
    path("<slug:slug>/", ProjectDetailView.as_view(), name="projects-detail"),
    path("<slug:slug>/edit/", ProjectUpdateView.as_view(), name="projects-edit"),
    path("<slug:slug>/delete/", ProjectDeleteView.as_view(), name="projects-delete"),
]
