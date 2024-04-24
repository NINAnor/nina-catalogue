from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from metadata_catalogue.maps.api import views

router = routers.DefaultRouter()
router.register(r"maps", views.MapViewSet, basename="maps")
router.register(r"raster-sources", views.RasterSourceViewSet, basename="raster-sources")
router.register(r"vector-sources", views.VectorSourceViewSet, basename="vector-sources")
router.register(r"layers", views.LayerViewSet, basename="layers")
router.register(r"layer-groups", views.LayerGroupViewSet, basename="layer-groups")


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + router.urls
