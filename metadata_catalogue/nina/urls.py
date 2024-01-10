from django.urls import path

from .views import DepartmentDetailView, DepartmentListView, ProjectDetailView, ProjectListView, ProjectUpdateView

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="projects-list"),
    path("projects/<str:pk>/", ProjectDetailView.as_view(), name="projects-detail"),
    path("projects/<str:pk>/edit/", ProjectUpdateView.as_view(), name="projects-edit"),
    path("departments/", DepartmentListView.as_view(), name="departments-list"),
    path("departments/<str:pk>/", DepartmentDetailView.as_view(), name="departments-detail"),
]
