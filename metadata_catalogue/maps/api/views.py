from django.db.models import Q
from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from ..enums import Visibility
from ..filters import PortalMapFilter
from ..libs.maplibre import MapStyle, map_to_style
from ..models import Layer, LayerGroup, Map, Portal, PortalMap, RasterSource, Source, VectorSource
from .serializers import (
    FileUploadSerializer,
    LayerGroupSerializer,
    LayerSerializer,
    MapSerializer,
    PortalMapSerializer,
    PortalSerializer,
    RasterSourceSerializer,
    SourceSerializer,
    VectorSourceSerializer,
)


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    lookup_field = "slug"

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action != "style":
            return qs

        expression = Q()
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                expression = Q(visibility=Visibility.PUBLIC) | Q(owner=self.request.user)
        else:
            expression = Q(visibility=Visibility.PUBLIC)

        return qs.filter(expression).prefetch_related("groups")  # .select_related('map', 'portal')

    @extend_schema(responses={"200": OpenApiResponse(response=MapStyle)})
    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def style(self, request, *args, **kwargs):
        obj = self.get_object()
        style = map_to_style(obj, request)
        return Response(data=style.model_dump(exclude_none=True, by_alias=True))


UPLOAD_REQUEST_SCHEMA = {
    "multipart/form-data": {
        "type": "object",
        "properties": {"field": {"type": "string"}, "file": {"type": "string", "format": "binary"}},
    }
}


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    lookup_field = "slug"
    serializer_class = SourceSerializer


class UploadableMixin:
    @action(detail=True, methods=["post"], parser_classes=(MultiPartParser,))
    def upload(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = request.FILES.get("file")
        field = serializer.validated_data.get("field")
        setattr(instance, field, file)
        instance.save()
        return Response(self.get_serializer_class()(instance).data)


class RasterSourceViewSet(UploadableMixin, viewsets.ModelViewSet):
    queryset = RasterSource.objects.all()
    lookup_field = "slug"
    serializer_class = RasterSourceSerializer

    @extend_schema(request=UPLOAD_REQUEST_SCHEMA, responses={"200": RasterSourceSerializer})
    @action(detail=True, methods=["post"], parser_classes=(MultiPartParser,))
    def upload(self, request, *args, **kwargs):
        return super().upload(request, *args, **kwargs)


class VectorSourceViewSet(UploadableMixin, viewsets.ModelViewSet):
    queryset = VectorSource.objects.all()
    serializer_class = VectorSourceSerializer
    lookup_field = "slug"

    @extend_schema(request=UPLOAD_REQUEST_SCHEMA, responses={"200": RasterSourceSerializer})
    @action(detail=True, methods=["post"], parser_classes=(MultiPartParser,))
    def upload(self, request, *args, **kwargs):
        return super().upload(request, *args, **kwargs)


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


class PortalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portal.objects.all()
    serializer_class = PortalSerializer
    lookup_field = "uuid"
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()

        expression = Q()
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                expression = Q(visibility=Visibility.PUBLIC) | Q(owner=self.request.user)
        else:
            expression = Q(visibility=Visibility.PUBLIC)

        return qs.filter(expression)


class PortalMapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PortalMap.objects.all().order_by("order")
    serializer_class = PortalMapSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PortalMapFilter

    def get_queryset(self):
        qs = super().get_queryset()

        expression = Q()
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                expression = Q(map__visibility=Visibility.PUBLIC) | Q(map__owner=self.request.user)
        else:
            expression = Q(map__visibility=Visibility.PUBLIC) & Q(portal__visibility=Visibility.PUBLIC)

        return qs.filter(expression).select_related("map", "portal")
