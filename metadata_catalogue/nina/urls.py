from django.urls import path

from .views import DepartmentDetailView, DepartmentListView, ProjectDetailView, ProjectListView, ProjectUpdateView

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="projects-list"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="projects-detail"),
    path("projects/<slug:slug>/edit/", ProjectUpdateView.as_view(), name="projects-edit"),
    path("departments/", DepartmentListView.as_view(), name="departments-list"),
    path("departments/<slug:slug>/", DepartmentDetailView.as_view(), name="departments-detail"),
]
