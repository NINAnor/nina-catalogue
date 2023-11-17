from django.urls import path, re_path

from .views import get_dataset_vrt_view

urlpatterns = [
    path("<uuid:dataset_uuid>/definition.vrt", get_dataset_vrt_view, name="get-dataset-vrt"),
]
