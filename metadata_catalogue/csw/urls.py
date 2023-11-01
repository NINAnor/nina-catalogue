from django.urls import path

from metadata_catalogue.csw import views

urlpatterns = [
    path("csw/", views.csw_invoke, name="csw"),
]
