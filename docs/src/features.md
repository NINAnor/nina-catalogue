# Software features
Here is a list of the features available in the metadata catalogue

## Metadata module
- Automatic ingestion of DWCA datasets published on IPT
- CSW support to explore/query datasets metadata
- Metadata exposed in ISO 19139


## Dataset module
Current:
- Expose vector datasets with OGC API - Features (via PyGEOAPI)
- Different GDAL providers supported (gpkg, shp, parquet, postgresql, csv)
- Support DWCA dataset
- Support on-the-fly operation on vectors

Not supported:
- Other OGC API standards (Coverage, Maps, Tiles, Processes, Records, Environmental Data Retrieval, STAC)


## Maps module
**NOTE**: The software is intended as a solution for displaying datasets on the web using cloud-optimized formats that don't require GIS servers.

Current:
- Display vector datasets (via PMTiles)
- Display raster datasets (via Cloud-Optimized GeoTIFF)
- Organize layers in hierarchy/groups
- Layer legends
- Download of the original dataset
- Style rendering of raster (via TiTiler)
- Style rendering of vectors (via Maplibre JS)
- Zoom to bounding box
- Description of each layer
- Description of each group
- Description of the map
- Custom logo, title
- Basemaps
- APIs for create, edit the map
- Limited UI for simple edit
- Basic info popup

Not supported:
- Query/filter datasets features
- Dynamic style change
- Dynamic datasets that change frequently
- Clusters
- Analysis


It's possible to (re)use the Maps module as a base and to customize it or to develop features based for projects with different requirements.
