from uuid import UUID

from ninja import Router

from . import models, schema

maps_router = Router()


# https://github.com/vitalik/django-ninja/issues/803 - by_alias is needed for dashed properties
@maps_router.get(
    "/maps/{map_uuid}/metadata/",
    response=schema.MapMetadata,
    url_name="map_metadata",
    by_alias=True,
    exclude_none=True,
)
def get_map_metadata(request, map_uuid: UUID):
    try:
        m = models.Map.objects.get(uuid=map_uuid)
        return m.get_metadata(request)
    except models.Map.DoesNotExist:
        return {}


@maps_router.get(
    "/maps/{map_uuid}/style/", response=schema.MapStyle, url_name="map_style", by_alias=True, exclude_none=True
)
def get_map_style(request, map_uuid: UUID):
    try:
        m = models.Map.objects.get(uuid=map_uuid)
        return m.get_style(request)
    except models.Map.DoesNotExist:
        return {}
