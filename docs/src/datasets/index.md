# Datasets
The Catalogue allows to define `Datasets`, each dataset is a set of data in a specific format with a set of metadata.
The Catalogue aims to support different type of `Dataset` from different sources, right now the following are supported:
- Dataset Types:
    - DarwinCORE Archives
- Sources:
    - IPT server

## Import
Datasets are retrived from sources using `harvesters`. Harvesters are python functions that can extract data from a source type and populate the database with the corresponding dataset and metadata.

## Metadata
Along with the dataset a set of metadata is stored in the database in a normalized way.

![Dataset](kroki-plantuml:./datasets.puml)


## Services and Protocols
To explore and navigate the datasets two services are provided:
- PyCSW (csw protocol)
- PyGeoAPI (OGC API)

### PyCSW
The metadata stored in the database are converted an XML in the `ISO 19139` format using `pygeometa`.
PyCSW is integrated in Django using a custom mapping, so that the metadata are read using the Django ORM instead of `SQL`.

**NOTE**: this implies that complex queries may not work as expected.

### PyGeoAPI
Datasets are shared through PyGeoAPI using GDAL as resource provider: this is implemented using GDAL `VRT` for vectors.

**NOTE**: raster support is missing

Each dataset should provide a valid `vrt` definition to open the file, this allows for example to serve CSV files as spatial datasets.
