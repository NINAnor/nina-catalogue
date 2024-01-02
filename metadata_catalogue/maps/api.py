import uuid
from typing import List

from django.db.models import Q
from ninja import Router
from ninja.responses import codes_4xx

from . import models, schema
from .enums import Visibility

maps_router = Router()


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
