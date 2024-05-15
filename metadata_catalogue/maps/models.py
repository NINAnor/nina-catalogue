import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django_lifecycle import BEFORE_CREATE, LifecycleModel, hook
from polymorphic.models import PolymorphicModel
from slugify import slugify
from treebeard.mp_tree import MP_Node

from .conf import settings
from .enums import Visibility


def layers_folder(instance, filename):
    return f"maps/sources/{instance.id}/{filename}"


def logo_folder(instance, filename):
    return f"maps/logo/{instance.slug}/{filename}"


def empty_json():
    return {}


class Source(PolymorphicModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(null=True, blank=True, max_length=250)
    extra = models.JSONField(default=empty_json, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    style = models.JSONField(default=empty_json, blank=True)
    metadata = models.JSONField(default=empty_json, blank=True)
    attribution = models.CharField(null=True, blank=True, max_length=250)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
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
    slug = models.SlugField(null=True, blank=True, max_length=250)
    map = models.ForeignKey("maps.Map", on_delete=models.CASCADE, related_name="layers")
    source = models.ForeignKey("maps.Source", on_delete=models.CASCADE, null=True, blank=True)
    source_layer = models.CharField(blank=True, null=True)
    style = models.JSONField(default=empty_json, blank=True)
    map_order = models.IntegerField(default=0)
    group = models.ForeignKey(
        "maps.LayerGroup", on_delete=models.SET_NULL, related_name="layers", null=True, blank=True
    )
    group_order = models.IntegerField(default=0)
    downloadable = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(null=True, blank=True)
    legend = models.JSONField(null=True, blank=True)
    is_basemap = models.BooleanField(default=False, verbose_name="Is basemap")
    is_lazy = models.BooleanField(default=True, verbose_name="Is lazy")
    hidden = models.BooleanField(default=True)
    metadata = models.JSONField(default=empty_json, blank=True)

    def __str__(self):
        return f"{self.slug} @ {self.map}"

    def get_download_url(self, request):
        if self.source and self.downloadable:
            return self.source.get_download_url(request)
        return None

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


class Map(LifecycleModel):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True, max_length=150)
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(blank=True)
    # center =
    zoom = models.IntegerField(null=True, blank=True)
    extra = models.JSONField(default=empty_json, blank=True)
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    visibility = models.CharField(default=Visibility.PRIVATE, max_length=10, choices=Visibility.choices)
    logo = models.ImageField(blank=True, null=True, upload_to=logo_folder)
    legend_config = models.JSONField(null=True, blank=True)
    basemap_config = models.JSONField(null=True, blank=True)
    config = models.JSONField(null=True, blank=True)

    @hook(BEFORE_CREATE)
    def generate_slug(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [models.UniqueConstraint("slug", name="map unique slug")]

    def get_metadata(self, request):
        layers = []
        lazy_layers = {}
        for root in self.groups.order_by("order").all():
            layers.append(root.as_layer_tree(request))

        style_url = request.build_absolute_uri(
            reverse(f"{settings.MAPS_API_PREFIX}:map_style", kwargs={"map_slug": self.slug})
        )

        for layer in self.layers.filter(is_basemap=False, is_lazy=True).order_by("map_order"):
            source = layer.source.get_real_instance() if layer.source else None

            lazy_layers[layer.slug] = {
                "id": layer.slug,
                "type": source.type,
                "metadata": {
                    "legend": layer.legend,
                    "name": layer.name,
                    "description": layer.description,
                },
            }

            if source and source.type:
                lazy_layers[layer.slug]["source"] = {
                    "type": source.type,
                    "url": source.get_source_url(request),
                }
            if source.attribution is not None:
                lazy_layers[layer.slug]["attribution"] = source.attribution

            if source and source.type and source.type == "vector" and layer.source_layer:
                lazy_layers[layer.slug]["source-layer"] = layer.source_layer

            for k, v in source.style.items():
                if v is not None:
                    lazy_layers[layer.slug][k] = v

            for k, v in layer.style.items():
                if v is not None:
                    lazy_layers[layer.slug][k] = v

        return {
            "style": style_url,
            "subtitle": self.subtitle,
            "title": self.title,
            "logo": request.build_absolute_uri(self.logo.url) if self.logo else None,
            "description": self.description,
            "layers": layers,
            "lazy": {"layers": lazy_layers},
        }

    def get_style(self, request):
        sources = {}
        layers = []

        for layer in self.layers.filter(models.Q(is_basemap=True) | models.Q(is_lazy=False)).order_by("map_order"):
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
                    "metadata": {
                        "legend": layer.legend,
                        "name": layer.name,
                        "description": layer.description,
                        "is_basemap": layer.is_basemap,
                    },
                    "source-layer": None
                    if not source or not source.type or source.type != "vector"
                    else layer.source_layer,
                    "layout": {
                        "visibility": "none" if layer.hidden else "visible",
                    },
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
            "metadata": {
                "legend": self.legend_config,
                "subtitle": self.subtitle,
                "title": self.title,
                "logo": request.build_absolute_uri(self.logo.url) if self.logo else None,
                "description": self.description,
                "basemaps": {
                    "config": self.basemap_config,
                },
                "config": self.config,
            },
            **self.extra,
        }


class LayerGroup(MP_Node):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True, max_length=250)
    order = models.IntegerField(default=0, blank=True)
    map = models.ForeignKey("maps.Map", on_delete=models.CASCADE, null=True, blank=True, related_name="groups")
    download_url = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(null=True, blank=True)

    node_order_by = ["order", "name"]

    class Meta:
        constraints = [models.UniqueConstraint("slug", name="group unique slug")]

    def __str__(self):
        return f"{self.name} @ {self.map}"

    def as_layer_tree(self, request):
        current_group = {
            "id": f"group-{self.id}",
            "name": self.name,
            "children": [],
            "download": self.download_url,
            "link": self.link,
            "description": self.description,
        }
        for sub_group in self.get_children():
            current_group["children"].append(sub_group.as_layer_tree(request))

        for layer in self.layers.select_related("source").order_by("group_order", "source__name"):
            current_group["children"].append(
                {
                    "id": layer.slug,
                    "name": str(layer.name),
                    "download": layer.get_download_url(request),
                    "link": layer.link,
                    "description": layer.description,
                }
            )

        return current_group


class Portal(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=250)
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.PRIVATE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    extra = models.JSONField(default=empty_json, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint("uuid", name="portal_unique_uuid"),
        ]

    def __str__(self) -> str:
        return self.title


class PortalMap(models.Model):
    map = models.ForeignKey("maps.Map", on_delete=models.CASCADE, related_name="portals")
    portal = models.ForeignKey("maps.Portal", on_delete=models.CASCADE, related_name="maps")
    order = models.IntegerField(default=0, blank=True)
    extra = models.JSONField(default=empty_json, blank=True)

    def __str__(self) -> str:
        return f"{self.map} @ {self.portal}"
