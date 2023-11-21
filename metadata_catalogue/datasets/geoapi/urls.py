from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "geoapi"

urlpatterns = [
    path("", views.landing_page, name="landing-page"),
    path("/openapi", views.openapi, name="openapi"),
    path("/conformance", views.conformance, name="conformance"),
    path("/collections", views.collections, name="collections"),
    path(
        "/collections/<str:collection_id>",
        views.collections,
        name="collection-detail",
    ),
    path(
        "/collections/<str:collection_id>/queryables",
        views.collection_queryables,
        name="collection-queryables",
    ),
    path(
        "/collections/<str:collection_id>/items",
        views.collection_items,
        name="collection-items",
    ),
    path(
        "/collections/<str:collection_id>/items/<str:item_id>",
        views.collection_item,
        name="collection-item",
    ),
    path(
        "/collections/<str:collection_id>/coverage",
        views.collection_coverage,
        name="collection-coverage",
    ),
    path(
        "/collections/<str:collection_id>/coverage/domainset",  # noqa
        views.collection_coverage_domainset,
        name="collection-coverage-domainset",
    ),
    path(
        "/collections/<str:collection_id>/coverage/rangetype",  # noqa
        views.collection_coverage_rangetype,
        name="collection-coverage-rangetype",
    ),
    path(
        "/collections/<str:collection_id>/map",
        views.collection_map,
        name="collection-map",
    ),
    path(
        "/collections/<str:collection_id>/styles/<str:style_id>/map",
        views.collection_style_map,
        name="collection-style-map",
    ),
    path(
        "/collections/<str:collection_id>/tiles",
        views.collection_tiles,
        name="collection-tiles",
    ),
    path(
        "/collections/<str:collection_id>/tiles/<str:tileMatrixSetId>",
        views.collection_tiles_metadata,
        name="collection-tiles-metadata",
    ),
    path(
        "/collections/<str:collection_id>/tiles/<str:tileMatrixSetId>/metadata",
        views.collection_tiles_metadata,
        name="collection-tiles-metadata",
    ),
    path(
        "/collections/<str:collection_id>/tiles/\
        <str:tileMatrixSetId>/<str:tile_matrix>/<str:tileRow>/<str:tileCol>",
        views.collection_item_tiles,
        name="collection-item-tiles",
    ),
    path(
        "/collections/<str:collection_id>/position",
        views.get_collection_edr_query,
        name="collection-edr-position",
    ),
    path(
        "/collections/<str:collection_id>/area",
        views.get_collection_edr_query,
        name="collection-edr-area",
    ),
    path(
        "/collections/<str:collection_id>/cube",
        views.get_collection_edr_query,
        name="collection-edr-cube",
    ),
    path(
        "/collections/<str:collection_id>/radius",
        views.get_collection_edr_query,
        name="collection-edr-radius",
    ),
    path(
        "/collections/<str:collection_id>/trajectory",
        views.get_collection_edr_query,
        name="collection-edr-trajectory",
    ),
    path(
        "/collections/<str:collection_id>/corridor",
        views.get_collection_edr_query,
        name="collection-edr-corridor",
    ),
    path(
        "/collections/<str:collection_id>/instances/<str:instance_id>/position",
        views.get_collection_edr_query,
        name="collection-edr-instance-position",
    ),
    path(
        "/collections/<str:collection_id>/instances/<str:instance_id>/area",
        views.get_collection_edr_query,
        name="collection-edr-instance-area",
    ),
    path(
        "/collections/<str:collection_id>/instances/<str:instance_id>/cube",
        views.get_collection_edr_query,
        name="collection-edr-instance-cube",
    ),
    path(
        "/collections/<str:collection_id>/instances/<str:instance_id>/radius",
        views.get_collection_edr_query,
        name="collection-edr-instance-radius",
    ),
    path(
        "/collections/<str:collection_id>/instances/<str:instance_id>/trajectory",  # noqa
        views.get_collection_edr_query,
        name="collection-edr-instance-trajectory",
    ),
    path(
        "/collections/<str:collection_id>/instances/<str:instance_id>/corridor",
        views.get_collection_edr_query,
        name="collection-edr-instance-corridor",
    ),
    path("/processes", views.processes, name="processes"),
    path("/processes/<str:process_id>", views.processes, name="process-detail"),
    path("/jobs/", views.jobs, name="jobs"),
    path("/jobs/<str:job_id>", views.jobs, name="job"),
    path(
        "/jobs/<str:job_id>/results",
        views.job_results,
        name="job-results",
    ),
    path(
        "/jobs/<str:job_id>/results/<str:resource>",
        views.job_results_resource,
        name="job-results-resource",
    ),
    path("/stac", views.stac_catalog_root, name="stac-catalog-root"),
    path("/stac/<str:path>", views.stac_catalog_path, name="stac-catalog-path"),
    path("/stac/search", views.stac_catalog_search, name="stac-catalog-search"),
]

# Add static URLs to serve pygeoapi statics
urlpatterns += static(settings.STATIC_URL, document_root=str(settings.APPS_DIR / "static" / "geoapi"))
