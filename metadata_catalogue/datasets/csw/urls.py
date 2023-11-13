from django.urls import path

from . import views

urlpatterns = [
    path("", views.csw_invoke, name="csw"),
]
