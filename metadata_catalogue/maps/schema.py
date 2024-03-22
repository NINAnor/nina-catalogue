import uuid
from typing import Dict, List, Optional

from django.conf import settings
from django.urls import reverse
from ninja import ModelSchema, Schema
from pydantic import Field, JsonValue

from . import models


# Maplibre Sources - https://maplibre.org/maplibre-style-spec/sources/
class Source(Schema):
    type: str
    tiles: list[str] | None = None
    url: str | None = None
    attribution: str | None = None
    bounds: list[float] | None = None
    maxzoom: str | None = None
    minzoom: str | None = None
    promoteId: str | dict[str, str] | None = None
    scheme: str | None = None
    volatile: bool | None = None
    tileSize: int | None = None


# Maplibre Layers - https://maplibre.org/maplibre-style-spec/layers/


# https://github.com/vitalik/django-ninja/issues/803 - populate_by_name is needed for dashed properties
class Layer(Schema):
    class Config:
        populate_by_name = True

    id: str
    type: str
    filter: JsonValue | None = None
    maxzoom: int | None = None
    minzoom: int | None = None
    metadata: JsonValue | None = None
    paint: JsonValue | None = None
    layout: JsonValue | None = None
    source: str | None = None
    source_layer: str | None = Field(alias="source-layer", default=None)


# Maplibre root - https://maplibre.org/maplibre-style-spec/root/
class MapStyle(Schema):
    version: int
    name: str | None = None
    zoom: int | None = None
    center: list[float] | None = None
    sources: dict[str, Source] | None = None
    layers: list[Layer] | None = None
    pitch: int | None = None
    metadata: JsonValue


# Custom
class LayerGroup(Schema):
    id: str
    name: str
    download: str | None = None
    children: list["LayerGroup"] | None = None
    link: str | None = None
    description: str | None = None


class MapMetadata(Schema):
    title: str
    style: str
    subtitle: str | None = None
    description: str | None = None
    layers: list[LayerGroup] | None = None
    logo: str | None = None
    lazy: JsonValue


class StatusMessage(Schema):
    message: str


class PortalMaps(Schema):
    slug: str = Field(alias="map.slug")
    title: str = Field(alias="map.title")
    subtitle: str = Field(alias="map.subtitle")
    logo: str | None
    description: str | None = Field(None, alias="map.description")
    visibility: str = Field("public", alias="map.visibility")
    extra: JsonValue
    url: str

    @staticmethod
    def resolve_url(obj, context):
        request = context.get("request")
        return request.build_absolute_uri(
            reverse(f"{settings.MAPS_API_PREFIX}:map_metadata", kwargs={"map_slug": obj.map.slug})
        )

    @staticmethod
    def resolve_logo(obj, context):
        request = context.get("request")
        return request.build_absolute_uri(obj.map.logo.url) if obj.map.logo else None


class Portal(Schema):
    title: str
    uuid: uuid.UUID
    extra: JsonValue


class RasterSourceSchema(ModelSchema):
    class Meta:
        model = models.RasterSource
        fields = [
            "id",
            "name",
            "slug",
            "protocol",
            "url",
            "attribution",
            "style",
            "extra",
            "original_data",
            "source",
        ]


class SourceSchema(ModelSchema):
    class Meta:
        model = models.Source
        fields = [
            "id",
            "name",
            "slug",
            "style",
            "extra",
        ]


class LayerSchema(ModelSchema):
    class Meta:
        model = models.Layer
        fields = "__all__"


class CreateLayerSchema(Schema):
    map_id: int
    source_id: int
    name: str
    slug: str
