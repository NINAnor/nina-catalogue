from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicChildModelFilter, PolymorphicParentModelAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import LayerGroup, LayerGroupItem, LayerSource, LayerStyle, Map, RasterLayer, VectorLayer


class LayerStyleInline(admin.TabularInline):
    model = LayerStyle


class LayerGroupsInline(admin.TabularInline):
    model = LayerGroup


class LayerGroupItemsInline(admin.TabularInline):
    model = LayerGroupItem


@admin.register(LayerGroup)
class LayerGroupAdmin(TreeAdmin):
    form = movenodeform_factory(LayerGroup)

    list_display = [
        "name",
        "map",
    ]

    list_filter = ["map"]

    inlines = [LayerGroupItemsInline]


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "subtitle",
    ]

    inlines = [LayerStyleInline, LayerGroupsInline]


@admin.register(LayerSource)
class LayerSourceAdmin(PolymorphicParentModelAdmin):
    base_model = LayerSource
    child_models = (RasterLayer, VectorLayer, LayerSource)
    list_filter = (PolymorphicChildModelFilter,)


class LayerSourceBaseAdmin(PolymorphicChildModelAdmin):
    base_model = LayerSource


@admin.register(VectorLayer)
class VectorLayerAdmin(LayerSourceBaseAdmin):
    base_model = VectorLayer


@admin.register(RasterLayer)
class RasterLayerAdmin(LayerSourceBaseAdmin):
    base_model = RasterLayer


@admin.register(LayerStyle)
class LayerStyleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "map",
        "source",
    ]
