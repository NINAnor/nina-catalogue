import logging
import traceback
from typing import Dict, List, Literal, Union

from django.contrib.gis.db.models import Extent
from django.db.models import Q
from pydantic import BaseModel, Field, JsonValue, ValidationError

from metadata_catalogue.maps.models import Map, Source


def hyphenize(field: str):
    return field.replace("_", "-")


# Maplibre Sources - https://maplibre.org/maplibre-style-spec/sources/
class MaplibreSource(BaseModel):
    class Config:
        alias_generator = hyphenize
        populate_by_name = True

    type: str
    tiles: list[str] | None = None
    url: str | None = None
    attribution: str | None = None
    bounds: list[float] | None = None
    maxzoom: int | None = None
    minzoom: int | None = None
    promoteId: str | dict[str, str] | None = None
    scheme: str | None = None
    volatile: bool | None = None
    tileSize: int | None = None


class ExtendedMaplibreSource(MaplibreSource):
    """
    Extends the MaplibreSource adding new fields
    this fields are not part of the specification
    """

    id: str


class IntervalLegendEntry(BaseModel):
    background: str
    description: str


class IntervalLegend(BaseModel):
    type: Literal["interval"]
    intervals: list[IntervalLegendEntry]

    id: str | None = None
    title: str | None = None


class SequentialLegend(BaseModel):
    type: Literal["sequential"]
    background: str
    min_label: str
    max_label: str
    vertical: bool = False

    id: str | None = None
    title: str | None = None


class WMSLegend(BaseModel):
    url: str
    type: Literal["wms"]
    id: str | None = None
    title: str | None = None


class LayerMetadata(BaseModel):
    name: str | None = None
    description: str | None = None
    is_basemap: bool
    legend: IntervalLegend | SequentialLegend | WMSLegend | None = None
    download: str | None = None


# Maplibre Layers - https://maplibre.org/maplibre-style-spec/layers/
# https://github.com/vitalik/django-ninja/issues/803 - populate_by_name is needed for dashed properties
class MaplibreLayer(BaseModel):
    class Config:
        alias_generator = hyphenize
        populate_by_name = True

    id: str
    type: str
    filter: JsonValue | None = None
    maxzoom: int | None = None
    minzoom: int | None = None
    metadata: LayerMetadata | None = None
    paint: JsonValue | None = None
    layout: JsonValue | None = None
    source: str | MaplibreSource | ExtendedMaplibreSource | None = None
    source_layer: str | None = None


class CatalogueTreeNode(BaseModel):
    """
    Describes a node or a leaf in the catalogue tree
    Nodes are LayerGroups
    Leafs are MapLayers
    """

    id: str
    name: str
    download: str | None = None
    children: list["CatalogueTreeNode"] | None = None
    link: str | None = None
    description: str | None = None
    is_open: bool = True
    bbox: list[float] | None = None


class MapConfig(BaseModel):
    exclusive_layers: bool = Field(default=False, description="Only one layer should be visible at a time")
    zoom_to_extent: bool = Field(default=False, description="Enable zoom to extend button")
    logo_layout: Literal["vertical"] | Literal["horizontal"] = "horizontal"
    layer_legend: bool = Field(default=True, description="Enable layer legend")


class MapCatalogue(BaseModel):
    """
    Describes the tree structure to load layers
    """

    tree: list["CatalogueTreeNode"] | None = None
    # should contain all the layers available in the map
    layers: dict[str, MaplibreLayer]
    basemaps_ids: list[str] | None = None


class MapMetadata(BaseModel):
    title: str
    subtitle: str | None = None
    description: str | None = None
    logo: str | None = None
    catalogue: MapCatalogue | None = None
    config: MapConfig = MapConfig()
    legends: IntervalLegend | SequentialLegend | None = None


# Maplibre root - https://maplibre.org/maplibre-style-spec/root/
class MapStyle(BaseModel):
    version: int
    name: str | None = None
    zoom: int | None = None
    center: list[float] | None = None
    sources: dict[str, MaplibreSource | ExtendedMaplibreSource] | None = None
    layers: list[MaplibreLayer] | None = None
    pitch: int | None = None
    metadata: MapMetadata


def map_to_style(map: Map, request) -> MapStyle:
    basemaps_ids = []
    layers = {}
    tree = []

    onload_sources = {}
    onload_layers = []

    sources = {o.pk: o for o in Source.objects.filter(layer__map=map).get_real_instances()}

    for layer in map.layers.order_by("map_order"):
        # extract the real instance (not the polymorphic parent)
        if layer.source_id:
            source = sources[layer.source_id]
        else:
            source = None

        maplibre_source = None

        if source:
            kwargs = {
                "id": source.id,
                "type": source.type,
                "url": source.get_source_url(request),
                "attribution": source.attribution,
                **source.extra,
            }
            try:
                maplibre_source = MaplibreSource(**kwargs)
            except ValidationError:
                logging.warning(f"Error while creating source for {layer.source_id}: {traceback.format_exc()}")

        # These arguments can be overrided
        extra_args = {
            "type": maplibre_source.type if maplibre_source and maplibre_source.type else "background",
            "layout": {"visibility": "none" if layer.hidden and not layer.is_lazy else "visible"},
            "attribution": source.attribution,
            **source.style,
            **layer.style,
        }

        maplibre_layer = MaplibreLayer(
            id=layer.slug,
            source=maplibre_source,
            source_layer=None if not source or not source.type or source.type != "vector" else layer.source_layer,
            metadata=LayerMetadata(
                name=layer.name,
                description=layer.description,
                is_basemap=layer.is_basemap,
                legend=layer.legend,
                download=source.get_download_url(request),
            ),
            **extra_args,
        )

        if layer.is_basemap or not layer.is_lazy:
            onload_sources[source.slug] = maplibre_source
            onload_layers.append(maplibre_layer.model_copy(update={"source": source.slug}))
        else:
            layers[layer.slug] = maplibre_layer

        if layer.is_basemap:
            # TODO: double check this!!
            basemaps_ids.append(layer.slug)

        # layers.append(
        #     {
        #         "id": layer.slug,
        #         "type": source.type,
        #         "source": None if not source or not source.type else source.slug,
        #         "metadata": {
        #             "legend": layer.legend,
        #             "name": layer.name,
        #             "description": layer.description,
        #             "is_basemap": layer.is_basemap,
        #         },
        #         "source-layer": None
        #         if not source or not source.type or source.type != "vector"
        #         else layer.source_layer,
        #         "layout": {
        #             "visibility": "none" if layer.hidden else "visible",
        #         },
        #         **source.style,
        #         **layer.style,
        #     }
        # )

    for root in map.groups.all().order_by("order"):
        # Precompute the extent list of all the nodes in the tree
        extents = {
            o["id"]: o["bbox_extent"]
            for o in root.get_tree().annotate(bbox_extent=Extent("bbox")).values("id", "bbox_extent")
        }
        tree.append(root.as_layer_tree(request, map, sources=sources, extents=extents))

    catalogue = MapCatalogue(
        basemaps_ids=basemaps_ids,
        layers=layers,
        tree=tree,
    )

    map_metadata = MapMetadata(
        title=map.title,
        subtitle=map.subtitle,
        description=map.description,
        logo=request.build_absolute_uri(map.logo.url) if map.logo else None,
        legends=map.legend_config,
        catalogue=catalogue,
        config=MapConfig(**map.config) if map.config else MapConfig(),
    )

    style = MapStyle(
        version=8,
        name=map.title,
        zoom=map.zoom,
        metadata=map_metadata,
        sources=onload_sources,
        layers=onload_layers,
        **map.extra,
    )

    return style
