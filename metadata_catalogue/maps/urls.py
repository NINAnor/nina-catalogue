from django.urls import path

from .views import ConfigJSView, PortalListPage, PortalPreview

app_name = "maps"

urlpatterns = [
    path(
        "<uuid:slug>/preview/config.js",
        ConfigJSView.as_view(),
        name="portal-preview-config",
    ),
    path(
        "<uuid:slug>/preview/",
        PortalPreview.as_view(),
        name="portal-preview",
    ),
    path("", PortalListPage.as_view(), name="portals-list"),
]
