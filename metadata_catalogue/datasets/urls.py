from django.urls import path
from . import views

urlpatterns = [
    path(
        "<uuid:dataset_uuid>/definition.vrt",
        views.get_dataset_vrt_view,
        name="get-dataset-vrt",
    ),
    path("", views.DatasetsListPage.as_view(), name="dataset-list"),
    path("create/", views.DatasetCreatePage.as_view(), name="dataset-create"),
    path("<uuid:slug>/", views.DatasetDetailPage.as_view(), name="dataset-detail"),
]
