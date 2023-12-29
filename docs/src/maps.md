# Maps module
Maps module provides a REST backend for displaying static maps, it implements the Maplibre spec and provides REST endpoints to:
- Get a portal
- List maps in a portal
- Get a map metadata
- Get a map style

## REST
A swagger endpoint is available at `/api/docs`, it provides a whole documentation of the data structures returned by the backend


## Terms
- *Portal*, is a set of maps, it represents a frontend implementing that specific portal
- *Map*, represents a singular Map entity, it's a set of layers sorted in a specific order with some styling. See: see: [Maplibre Root Spec](https://maplibre.org/maplibre-style-spec/root/)
- *Group*, represents a group of *Layers*, it is used as a building-block to create a hierarchical legend
- *Layer*, represents a single layer that will be shown in a map, see: [Maplibre Layer Spec](https://maplibre.org/maplibre-style-spec/layers/)
- *Source*, represents the source dataset itself, for example a `WMS` remote service or a `geojson` endpoint. See: [Maplibre Sources Spec](https://maplibre.org/maplibre-style-spec/sources/)


## Entity Relationships
![Map module architecture](kroki-plantuml:./maps.puml)


## Data Sources

### Vector
Vector data sources can be uploaded as `PMTiles`, a spatial file format that allows to serve `Cloud Optimized` vectors as single files that are dynamically fetched by the browser using `Http Range requests`. See [PMTiles Docs](https://github.com/protomaps/PMTiles) for more info about them.

**NOTE**: the frontend map should add `pmtiles` protocol

PMTiles files must be pre-processed before uploading to the maps module. Along with the PMTiles it's possible to upload also the original dataset in a different file format. This will be used when user ask for download, while PMTiles is used to display the dataset.

### Raster
Raster data sources can be uploaded as `Cloud Optimized GeoTIFF(COG)`, a spatial file format that allows to serve `Cloud Optimized` tiff as single files that are dynamically fetched by the browser using `Http Range requests`. See [COG Docs](https://www.cogeo.org/) for more info about them.

**NOTE**: the frontend map should add `cog` protocol

COG files must be pre-processed before uploading to the maps module. Along with the COG it's possible to upload also the original dataset in a different file format. This will be used when user ask for download, while COG is used to display the dataset.

- See [cog-tools](https://github.com/NINAnor/cog-tools) for tools to create a valid COG
- See [maplibre-gl-cog](https://github.com/NINAnor/maplibre-gl-cog) for displaying COG on maplibre

## Portal
a list of portals that use the map module:
- [Maps NINA](https://maps.nina.no) - code [Github](https://github.com/NINAnor/nina-map-explorer)
