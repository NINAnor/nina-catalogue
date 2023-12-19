from typing import Dict

from django.db import transaction
from slugify import slugify

from ..models import Layer, LayerGroup, Map, RasterSource, Source, VectorSource


def map_from_maplibre_style_spec(map_name: str, style: dict):
    with transaction.atomic():
        extra = {}
        if "center" in style:
            extra["center"] = style["center"]

        map = Map.objects.create(
            title=style.get("name", map_name),
            slug=slugify(style.get("name", map_name)),
            zoom=style.get("zoom", None),
            extra=extra,
        )

        entities = {}

        for key, source in style.get("sources").items():
            source_attrs = {"name": key, "slug": slugify(key), "extra": {}}
            source_type = source.get("type")

            if source_type == "vector":
                if "url" in source and "pmtiles://" in source.get("url"):
                    source_attrs["protocol"] = "pmtiles://"
                    source_attrs["url"] = source.get("url").replace("pmtiles://", "")

                source_attrs["attribution"] = source.get("attribution")
                entities[key] = VectorSource.objects.create(
                    **source_attrs,
                )
            elif source_type == "raster":
                if "url" in source and "cog://" in source.get("url"):
                    source_attrs["protocol"] = "cog://"
                    source_attrs["url"] = source.get("url").replace("cog://", "")
                source_attrs["attribution"] = source.get("attribution")
                if "tiles" in source:
                    source_attrs["extra"]["tiles"] = source["tiles"]
                if "tileSize" in source:
                    source_attrs["extra"]["tileSize"] = source["tileSize"]

                entities[key] = RasterSource.objects.create(
                    **source_attrs,
                )
            else:
                entities[key] = Source.objects.create(**source_attrs)

        group = LayerGroup.objects.create(name="Layers", order=0, map=map, download_url=None)

        for i, layer in enumerate(style.get("layers")):
            layer_attrs = {
                "style": {},
                "map_order": i,
                "slug": slugify(layer["id"]),
                "name": layer["id"],
                "map": map,
            }

            if "paint" in layer:
                layer_attrs["style"]["paint"] = layer["paint"]

            if "type" in layer:
                layer_attrs["style"]["type"] = layer["type"]

            if "layout" in layer:
                layer_attrs["style"]["layout"] = layer["layout"]

            if "source" in layer:
                layer_attrs["source"] = entities[layer["source"]]
                layer_attrs["group"] = group
                layer_attrs["group_order"] = i

            if "source-layer" in layer:
                layer_attrs["source_layer"] = layer["source-layer"]

            Layer.objects.create(**layer_attrs)
