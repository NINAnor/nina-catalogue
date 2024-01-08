from django.urls import path

from .views import ProjectDetailView, ProjectListView, ProjectUpdateView

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="projects-list"),
    path("projects/<int:extid>/", ProjectDetailView.as_view(), name="projects-detail"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="projects-detail"),
    path("projects/<slug:slug>/edit/", ProjectUpdateView.as_view(), name="projects-edit"),
]
