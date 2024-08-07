from rest_framework import serializers

from ..models import Layer, LayerGroup, Map, Portal, PortalMap, RasterSource, Source, VectorSource


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    field = serializers.CharField(required=True)


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = [
            "slug",
            "id",
            "title",
            "subtitle",
            "zoom",
            "description",
            "visibility",
            "config",
            "legend_config",
            "basemap_config",
        ]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = [
            "name",
            "slug",
            "extra",
            "style",
            "attribution",
            "metadata",
        ]


class RasterSourceBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasterSource
        fields = [
            "name",
            "slug",
            "extra",
            "style",
            "url",
            "attribution",
            "protocol",
            "metadata",
        ]


class RasterSourceSerializer(serializers.ModelSerializer):
    class Meta(RasterSourceBaseSerializer.Meta):
        fields = [
            "name",
            "slug",
            "extra",
            "style",
            "url",
            "attribution",
            "protocol",
            "source",
            "original_data",
            "metadata",
        ]


class VectorSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorSource
        fields = [
            "name",
            "slug",
            "extra",
            "style",
            "url",
            "attribution",
            "protocol",
            "source",
            "original_data",
            "default_layer",
            "metadata",
        ]


class LayerSerializer(serializers.ModelSerializer):
    map = serializers.SlugRelatedField(slug_field="slug", queryset=Map.objects.all())
    source = serializers.SlugRelatedField(slug_field="slug", queryset=Source.objects.all())
    group = serializers.SlugRelatedField(slug_field="slug", queryset=LayerGroup.objects.all())

    class Meta:
        model = Layer
        fields = [
            "name",
            "slug",
            "map",
            "source",
            "source_layer",
            "style",
            "group",
            "group_order",
            "downloadable",
            "description",
            "link",
            "legend",
            "is_basemap",
            "is_lazy",
            "hidden",
            "metadata",
        ]


class LayerGroupSerializer(serializers.ModelSerializer):
    map = serializers.SlugRelatedField(slug_field="slug", queryset=Map.objects.all(), allow_null=True, required=False)
    parent = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=LayerGroup.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = LayerGroup
        fields = [
            "name",
            "order",
            "slug",
            "map",
            "description",
            "link",
            "download_url",
            "parent",
        ]

    def create(self, validated_data):
        parent = validated_data.pop("parent")
        if parent:
            return parent.add_child(**validated_data)
        else:
            return LayerGroup.add_root(**validated_data)


class MapMetadataSerializer(serializers.HyperlinkedModelSerializer):
    style = serializers.HyperlinkedIdentityField(view_name="maps-style", lookup_field="slug")

    class Meta:
        model = Map
        fields = [
            "slug",
            "title",
            "subtitle",
            "logo",
            "style",
            "visibility",
        ]


class PortalMapSerializer(serializers.ModelSerializer):
    map = MapMetadataSerializer()

    class Meta:
        model = PortalMap
        fields = [
            "map",
            "order",
            "extra",
            "external_title",
            "external_subtitle",
            "external_cover",
            "external_link",
        ]


class PortalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portal
        fields = ["uuid", "title", "extra", "visibility"]
