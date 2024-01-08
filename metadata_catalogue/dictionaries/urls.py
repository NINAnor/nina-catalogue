from django.urls import path

from .views import SPARQLView

urlpatterns = [
    path("sparql/", SPARQLView.as_view(), name="sparql"),
]
