from ..libs.maplibre import (
    CatalogueTreeNode,
    ExtendedMaplibreSource,
    IntervalLegend,
    IntervalLegendEntry,
    LayerMetadata,
    MapCatalogue,
    MapConfig,
    MaplibreLayer,
    MaplibreSource,
    MapMetadata,
    MapStyle,
    SequentialLegend,
)


def postprocessing(result, generator, request, public):
    definitions = result.setdefault("definitions", {})
    classes = [
        MapStyle,
        SequentialLegend,
        IntervalLegend,
        IntervalLegendEntry,
        CatalogueTreeNode,
        MapCatalogue,
        ExtendedMaplibreSource,
        LayerMetadata,
        MaplibreLayer,
        MaplibreSource,
        MapConfig,
        MapMetadata,
    ]

    for c in classes:
        definitions[c.__name__] = c.model_json_schema()

    return result
