from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicChildModelFilter, PolymorphicParentModelAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Layer, LayerGroup, Map, Portal, PortalMap, RasterSource, Source, VectorSource


class LayerInline(admin.TabularInline):
    model = Layer


class PortalMapInline(admin.TabularInline):
    model = PortalMap


@admin.register(LayerGroup)
class LayerGroupAdmin(TreeAdmin):
    form = movenodeform_factory(LayerGroup)

    list_display = [
        "name",
        "map",
    ]

    list_filter = ["map"]
    inlines = [LayerInline]


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "subtitle",
    ]

    inlines = [LayerInline]


@admin.register(Source)
class SourceAdmin(PolymorphicParentModelAdmin):
    base_model = Source
    child_models = (RasterSource, VectorSource, Source)
    list_filter = (PolymorphicChildModelFilter,)

    list_display = [
        "id",
        "name",
        "slug",
    ]


class SourceBaseAdmin(PolymorphicChildModelAdmin):
    base_model = Source


@admin.register(VectorSource)
class VectorSourceAdmin(SourceBaseAdmin):
    base_model = VectorSource

    list_display = [
        "id",
        "name",
        "slug",
        "protocol",
    ]


@admin.register(RasterSource)
class RasterSourceAdmin(SourceBaseAdmin):
    base_model = RasterSource

    list_display = [
        "id",
        "name",
        "slug",
        "protocol",
    ]


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "map",
        "source",
        "map_order",
        "group",
        "group_order",
    ]


@admin.register(Portal)
class PortalAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "visibility",
        "uuid",
    ]

    search_fields = [
        "title",
        "uuid",
    ]

    list_filter = [
        "visibility",
    ]

    inlines = [
        PortalMapInline,
    ]


@admin.register(PortalMap)
class PortalMapAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "portal",
        "map",
        "order",
    ]
