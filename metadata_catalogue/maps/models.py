import uuid

from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel
from slugify import slugify
from treebeard.mp_tree import MP_Node

from .conf import settings


def layers_folder(instance, filename):
    return f"maps/layers/{instance.id}/{filename}"


def empty_json():
    return {}


class LayerSource(PolymorphicModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(null=True)
    extra = models.JSONField(default=empty_json, blank=True)
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    style = models.JSONField(default=empty_json, blank=True)

    def get_slug(self):
        if self.slug:
            return self.slug
        else:
            self.slug = slugify(self.name)
            self.save(update_fields=["slug"])
            return self.slug

    @property
    def type(self):
        return None

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint("name", name="layer with unique name"),
            models.UniqueConstraint("slug", name="layer with unique slug"),
        ]

    def get_download_url(self):
        return None

    def get_source_url(self):
        return None


class RasterLayer(LayerSource):
    source = models.FileField(upload_to=layers_folder, null=True, blank=True)
    original_data = models.FileField(upload_to=layers_folder, null=True, blank=True)
    protocol = models.CharField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    attribution = models.CharField(null=True, blank=True, max_length=250)

    def get_download_url(self):
        return self.original_data.url if self.original_data else self.url

    def get_source_url(self):
        return self.source.url if self.source else self.url

    @property
    def type(self):
        return "raster"


class VectorLayer(LayerSource):
    source = models.FileField(upload_to=layers_folder, null=True, blank=True)
    original_data = models.FileField(upload_to=layers_folder, null=True, blank=True)
    protocol = models.CharField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    attribution = models.CharField(null=True, blank=True, max_length=250)

    def get_download_url(self):
        return self.original_data.url if self.original_data else self.url

    def get_source_url(self):
        return self.source.url if self.source else self.url

    @property
    def type(self):
        return "vector"


class LayerStyle(models.Model):
    name = models.CharField(null=True, blank=True, max_length=150)
    map = models.ForeignKey("maps.Map", on_delete=models.CASCADE, related_name="layers_style")
    source = models.ForeignKey("maps.LayerSource", on_delete=models.CASCADE, null=True, blank=True)
    style = models.JSONField(default=empty_json, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} @ {self.map}" if self.name else f"{self.source} @ {self.map}"


class Map(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(blank=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    # center =
    zoom = models.IntegerField(null=True, blank=True)
    extra = models.JSONField(default=empty_json, blank=True)
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [models.UniqueConstraint("uuid", name="map unique uuid")]

    def get_metadata(self, request):
        layers = []
        for root in self.groups.order_by("-order").all():
            layers.append(root.as_layer_tree())

        return {
            "style": reverse(f"{settings.MAPS_API_PREFIX}:map_metadata", kwargs={"map_uuid": self.uuid}),
            "subtitle": self.subtitle,
            "description": self.description,
            "layers": layers,
        }

    def get_style(self, request):
        sources = {}
        layers = []

        for style in self.layers_style.order_by("order"):
            source = LayerSource.objects.filter(id=style.source_id).get_real_instances()[0] if style.source else None
            if source and source.type:
                sources[source.get_slug()] = {
                    "type": source.type,
                    "url": source.get_source_url(),
                    "attribution": source.attribution,
                    **source.extra,
                }

            layers.append(
                {
                    "id": source.get_slug(),
                    "type": source.type,
                    "source": None if not source or not source.type else source.get_slug(),
                    "source-layer": None
                    if not source or not source.type or source.type != "vector"
                    else source.get_slug(),
                    **source.style,
                    **style.style,
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


class LayerGroupItem(models.Model):
    layer = models.ForeignKey("maps.LayerSource", on_delete=models.CASCADE)
    group = models.ForeignKey("maps.LayerGroup", on_delete=models.CASCADE, related_name="layer_items")
    order = models.IntegerField(default=0, blank=True)


class LayerGroup(MP_Node):
    name = models.CharField(max_length=150)
    order = models.IntegerField(default=0, blank=True)
    map = models.ForeignKey("maps.Map", on_delete=models.CASCADE, null=True, blank=True, related_name="groups")
    download_url = models.URLField(null=True, blank=True)
    layers = models.ManyToManyField("maps.LayerSource", through="maps.LayerGroupItem", related_name="layers")

    node_order_by = ["order", "name"]

    def __str__(self):
        return self.name

    def as_layer_tree(self):
        current_group = {"id": f"group-{self.id}", "name": self.name, "children": [], "download": self.download_url}
        for sub_group in self.get_children():
            current_group["children"].append(sub_group.as_layer_tree())

        for layer_item in self.layer_items.select_related("layer").order_by("-order", "-layer__name"):
            current_group["children"].append(
                {
                    "id": layer_item.layer.get_slug(),
                    "name": str(layer_item.layer.name),
                    "download": None,
                }
            )

        return current_group
