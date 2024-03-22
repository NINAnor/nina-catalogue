import uuid
from typing import List

from django.db.models import Q
from ninja import Router
from ninja.files import UploadedFile
from ninja.responses import codes_4xx
from ninja.security import APIKeyHeader

from . import models, schema
from .conf import settings
from .enums import Visibility

maps_router = Router()


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if settings.MAPS_API_KEY and settings.MAPS_API_KEY == key:
            return key


auth = [ApiKey()]


# https://github.com/vitalik/django-ninja/issues/803 - by_alias is needed for dashed properties
@maps_router.get(
    "/maps/{map_slug}/metadata/",
    response={
        200: schema.MapMetadata,
        codes_4xx: schema.StatusMessage,
    },
    url_name="map_metadata",
    by_alias=True,
    exclude_none=True,
)
def get_map_metadata(request, map_slug: str):
    try:
        m = models.Map.objects.get(slug=map_slug)
        if not request.user.has_perm("maps.map_view", m):
            return 404, {"message": "Not found"}
        return 200, m.get_metadata(request)
    except models.Map.DoesNotExist:
        return 404, {"message": "Not found"}


@maps_router.get(
    "/maps/{map_slug}/style/",
    response={200: schema.MapStyle, codes_4xx: schema.StatusMessage},
    url_name="map_style",
    by_alias=True,
    exclude_none=True,
)
def get_map_style(request, map_slug: str):
    try:
        m = models.Map.objects.get(slug=map_slug)
        if not request.user.has_perm("maps.map_view", m):
            return 404, {"message": "Not found"}
        return 200, m.get_style(request)
    except models.Map.DoesNotExist:
        return 404, {"message": "Not found"}


@maps_router.get(
    "/portals/{portal_uuid}/",
    response={200: schema.Portal, codes_4xx: schema.StatusMessage},
    url_name="portals_get",
    by_alias=True,
    exclude_none=True,
)
def get_portal(request, portal_uuid: uuid.UUID):
    try:
        portal = models.Portal.objects.get(uuid=portal_uuid)
        if not request.user.has_perm("maps.portal_view", portal):
            return 404, {"message": "Not found"}
        return 200, portal
    except models.Portal.DoesNotExist:
        return 404, {"message": "Not found"}


@maps_router.get(
    "/portals/{portal_uuid}/maps/",
    response={200: list[schema.PortalMaps], codes_4xx: schema.StatusMessage},
    url_name="portals_get_maps",
    exclude_none=True,
)
def get_portal_maps(request, portal_uuid: uuid.UUID):
    try:
        portal = models.Portal.objects.get(uuid=portal_uuid)
        if not request.user.has_perm("maps.portal_view", portal):
            return 404, {"message": "Not found"}

        expression = Q()
        if request.user.is_authenticated:
            if not request.user.is_staff:
                expression = Q(map__visibility=Visibility.PUBLIC) | Q(map__owner=request.user)
        else:
            expression = Q(map__visibility=Visibility.PUBLIC)
        return 200, portal.maps.filter(expression).select_related("map")
    except models.Portal.DoesNotExist:
        return 404, {"message": "Not found"}


@maps_router.get(
    "/sources/",
    response={200: list[schema.SourceSchema], codes_4xx: schema.StatusMessage},
    url_name="sources_list",
    auth=auth,
)
def get_sources_list(request):
    return models.Source.objects.all()


@maps_router.get(
    "/sources/raster/",
    response={200: list[schema.RasterSourceSchema], codes_4xx: schema.StatusMessage},
    url_name="sources_raster_list",
    auth=auth,
)
def get_sources_raster_list(request):
    return models.RasterSource.objects.all()


@maps_router.post(
    "/sources/raster/",
    response={201: schema.RasterSourceSchema, codes_4xx: schema.StatusMessage},
    url_name="sources_raster_create",
    auth=auth,
)
def create_raster_source(request, data: schema.RasterSourceSchema):
    return 201, models.RasterSource.objects.create(owner=None, **data.dict())


@maps_router.get(
    "/sources/raster/{source_slug}/",
    response={200: schema.RasterSourceSchema, codes_4xx: schema.StatusMessage},
    url_name="sources_raster_detail",
    auth=auth,
)
def get_sources_raster_detail(request, source_slug: str):
    try:
        return models.RasterSource.objects.get(slug=source_slug)
    except models.RasterSource.DoesNotExist:
        return 404, {"message": "Not found"}


@maps_router.post(
    "/sources/raster/{source_slug}/upload/{field}/",
    response={200: schema.RasterSourceSchema, codes_4xx: schema.StatusMessage},
    url_name="sources_raster_upload",
    auth=auth,
)
def upload_sources_raster(request, source_slug: str, file: UploadedFile, field: str):
    try:
        obj = models.RasterSource.objects.get(slug=source_slug)
        setattr(obj, field, file)
        obj.save()
        return obj
    except models.RasterSource.DoesNotExist:
        return 404, {"message": "Not found"}


@maps_router.get(
    "/sources/{source_slug}/",
    response={200: schema.SourceSchema, codes_4xx: schema.StatusMessage},
    url_name="sources_detail",
    auth=auth,
)
def get_sources_detail(request, source_slug: str):
    try:
        return models.Source.objects.get(slug=source_slug)
    except models.Source.DoesNotExist:
        return 404, {"message": "Not found"}


@maps_router.get(
    "/layers/",
    response={200: list[schema.LayerSchema], codes_4xx: schema.StatusMessage},
    url_name="layers_list",
    auth=auth,
)
def get_layer_list(request):
    return models.Layer.objects.all()


@maps_router.get(
    "/layers/{layer_slug}/",
    response={200: schema.RasterSourceSchema, codes_4xx: schema.StatusMessage},
    url_name="sources_raster_detail",
    auth=auth,
)
def get_layer_detail(request, layer_slug: str):
    try:
        return models.Layer.objects.get(slug=layer_slug)
    except models.Layer.DoesNotExist:
        return 404, {"message": "Not found"}


@maps_router.post(
    "/layers/",
    response={201: schema.RasterSourceSchema, codes_4xx: schema.StatusMessage},
    url_name="layers_create",
    auth=auth,
)
def create_layer(request, data: schema.LayerSchema):
    return 201, models.Layer.objects.create(**data.dict())
