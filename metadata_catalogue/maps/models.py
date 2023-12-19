from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel
from slugify import slugify
from treebeard.mp_tree import MP_Node

from .conf import settings


def layers_folder(instance, filename):
    return f"maps/sources/{instance.id}/{filename}"


def empty_json():
    return {}


class Source(PolymorphicModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(null=True, blank=True)
    extra = models.JSONField(default=empty_json, blank=True)
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    style = models.JSONField(default=empty_json, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def type(self):
        return None

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint("name", name="source with unique name"),
            models.UniqueConstraint("slug", name="source with unique slug"),
        ]

    def get_download_url(self, request):
        return None

    def get_source_url(self, request):
        return None


class RasterSource(Source):
    source = models.FileField(upload_to=layers_folder, null=True, blank=True)
    original_data = models.FileField(upload_to=layers_folder, null=True, blank=True)
    protocol = models.CharField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    attribution = models.CharField(null=True, blank=True, max_length=250)

    def get_download_url(self, request):
        return request.build_absolute_uri(self.original_data.url) if self.original_data else self.url

    def get_source_url(self, request):
        url = request.build_absolute_uri(self.source.url) if self.source else self.url
        return f"{self.protocol}{url}" if self.protocol and url else url

    @property
    def type(self):
        return "raster"


class VectorSource(Source):
    source = models.FileField(upload_to=layers_folder, null=True, blank=True)
    original_data = models.FileField(upload_to=layers_folder, null=True, blank=True)
    protocol = models.CharField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    attribution = models.CharField(null=True, blank=True, max_length=250)

    default_layer = models.CharField(null=True, blank=True)

    def get_download_url(self, request):
        return request.build_absolute_uri(self.original_data.url) if self.original_data else self.url

    def get_source_url(self, request):
        url = request.build_absolute_uri(self.source.url) if self.source else self.url
        return self.protocol + url if self.protocol and url else url

    @property
    def type(self):
        return "vector"


class Layer(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    map = models.ForeignKey("maps.Map", on_delete=models.CASCADE, related_name="layers")
    source = models.ForeignKey("maps.Source", on_delete=models.CASCADE, null=True, blank=True)
    source_layer = models.CharField(blank=True, null=True)
    style = models.JSONField(default=empty_json, blank=True)
    map_order = models.IntegerField(default=0)
    group = models.ForeignKey(
        "maps.LayerGroup", on_delete=models.SET_NULL, related_name="layers", null=True, blank=True
    )
    group_order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.slug} @ {self.map}"

    def save(self, *args, **kwargs):
        if self.slug is None:
            if self.source:
                self.slug = self.source.slug
            else:
                self.slug = "baselayer"

        if self.name is None:
            if self.source:
                self.name = self.source.name
            else:
                self.name = "Unnamed"

        if self.source and not self.source_layer:
            source = self.source.get_real_instance()
            if source.type == "vector":
                self.source_layer = source.default_layer

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slug", "map"], name="layer with unique slug"),
        ]


class Map(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(blank=True)
    # center =
    zoom = models.IntegerField(null=True, blank=True)
    extra = models.JSONField(default=empty_json, blank=True)
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [models.UniqueConstraint("slug", name="map unique slug")]

    def get_metadata(self, request):
        layers = []
        for root in self.groups.order_by("-order").all():
            layers.append(root.as_layer_tree())

        style_url = request.build_absolute_uri(
            reverse(f"{settings.MAPS_API_PREFIX}:map_style", kwargs={"map_slug": self.slug})
        )

        return {
            "style": style_url,
            "subtitle": self.subtitle,
            "description": self.description,
            "layers": layers,
        }

    def get_style(self, request):
        sources = {}
        layers = []

        for layer in self.layers.order_by("map_order"):
            source = layer.source.get_real_instance() if layer.source else None
            if source and source.type:
                sources[source.slug] = {
                    "type": source.type,
                    "url": source.get_source_url(request),
                    "attribution": source.attribution,
                    **source.extra,
                }

            layers.append(
                {
                    "id": layer.slug,
                    "type": source.type,
                    "source": None if not source or not source.type else source.slug,
                    "source-layer": None
                    if not source or not source.type or source.type != "vector"
                    else layer.source_layer,
                    **source.style,
                    **layer.style,
                }
            )

        return {
            "version": 8,
            "name": self.title,
            "zoom": self.zoom,
            "layers": layers,
            "sources": sources,
            **self.extra,
        }


class LayerGroup(MP_Node):
    name = models.CharField(max_length=150)
    order = models.IntegerField(default=0, blank=True)
    map = models.ForeignKey("maps.Map", on_delete=models.CASCADE, null=True, blank=True, related_name="groups")
    download_url = models.URLField(null=True, blank=True)

    node_order_by = ["order", "name"]

    def __str__(self):
        return f"{self.name} @ {self.map}"

    def as_layer_tree(self):
        current_group = {"id": f"group-{self.id}", "name": self.name, "children": [], "download": self.download_url}
        for sub_group in self.get_children():
            current_group["children"].append(sub_group.as_layer_tree())

        for layer in self.layers.select_related("source").order_by("group_order", "source__name"):
            current_group["children"].append(
                {
                    "id": layer.slug,
                    "name": str(layer.name),
                    "download": None,
                }
            )

        return current_group
