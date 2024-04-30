from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from ..models import Layer, LayerGroup, Map, RasterSource, VectorSource
from .serializers import (
    FileUploadSerializer,
    LayerGroupSerializer,
    LayerSerializer,
    MapSerializer,
    RasterSourceSerializer,
    VectorSourceSerializer,
)


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    lookup_field = "slug"


UPLOAD_REQUEST_SCHEMA = {
    "multipart/form-data": {
        "type": "object",
        "properties": {"field": {"type": "string"}, "file": {"type": "string", "format": "binary"}},
    }
}


class UploadableMixin:
    @action(detail=True, methods=["post"], parser_classes=(MultiPartParser,), serializer_class=FileUploadSerializer)
    def upload(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = request.FILES.get("file")
        field = serializer.validated_data.get("field")
        setattr(instance, field, file)
        instance.save()
        return instance


class RasterSourceViewSet(UploadableMixin, viewsets.ModelViewSet):
    queryset = RasterSource.objects.all()
    lookup_field = "slug"
    serializer_class = RasterSourceSerializer

    @extend_schema(request=UPLOAD_REQUEST_SCHEMA, responses={"200": RasterSourceSerializer})
    @action(detail=True, methods=["post"], parser_classes=(MultiPartParser,), serializer_class=FileUploadSerializer)
    def upload(self, request):
        return super().upload(request)


class VectorSourceViewSet(UploadableMixin, viewsets.ModelViewSet):
    queryset = VectorSource.objects.all()
    serializer_class = VectorSourceSerializer
    lookup_field = "slug"

    @extend_schema(request=UPLOAD_REQUEST_SCHEMA, responses={"200": RasterSourceSerializer})
    @action(detail=True, methods=["post"], parser_classes=(MultiPartParser,), serializer_class=FileUploadSerializer)
    def upload(self, request):
        return super().upload(request)


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Layer.objects.select_related("map").filter(map__slug=self.kwargs["map_slug"])


class LayerGroupViewSet(viewsets.ModelViewSet):
    queryset = LayerGroup.objects.all()
    serializer_class = LayerGroupSerializer
    lookup_field = "slug"
