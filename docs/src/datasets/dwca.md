# DarwinCORE Archives
Darwincore archives are zip files that contains certain files:
- eml.xml, contains the metadata
- meta.xml, contains info about all the other files inside the zip

This page explains the code in `datasets/libs/darwincore`.


Meta XML have a `core` and multiple optional `extensions`, each of them are related to files in the zip.
Every `ID` of each extension is the foreing key to the `core`.

Since DarwinCORE files are CSV, we have to identify which fields contains the geometry data. Right now are supported:
- `footprintWKT`
- `decimalLatitude`, `decimalLongitude`

The dataset import should read the content of `meta.xml` to generate a valid `vrt`. Here is an example, but specific code can be found in `metadata_catalogue/templates/vrt/definition.xml`.

```xml
<OGRVRTDataSource>
    <OGRVRTLayer name="data">
      <SrcDataSource><![CDATA[
        <OGRVRTDataSource>
          <OGRVRTLayer name="occurrence">
            <SrcDataSource>CSV:/vsizip/{/vsicurl/https://ipt.nina.no/archive.do?r=5912basidiomycetes}/occurrence.txt</SrcDataSource>
            <LayerSRS>WGS84</LayerSRS>
          </OGRVRTLayer>
        </OGRVRTDataSource>]]>
      </SrcDataSource>
      <SrcSQL>select * from occurrence</SrcSQL>

      <GeometryField encoding="PointFromColumns" x="decimalLongitude" y="decimalLatitude" reportSrcColumn="false">
        <GeometryType>wkbPoint</GeometryType>
        <SRS>WGS84</SRS>
      </GeometryField>
      
      <LayerSRS>WGS84</LayerSRS>
    </OGRVRTLayer>
  </OGRVRTDataSource>
```

Notes about GDAL:
- `CSV:` means that what is following must be treated as a CSV file
- `/vsizip/{}/occurrence.txt` means that the file we are looking for is inside a zip 
- `/vsicurl/https://ipt.nina.no/archive.do?r=5912basidiomycetes` means that the zipfile itself is a remote zipfile, downloadable from that URL
- `SrcSQL` allows `join` between data sources
- `SrcDataSource` allows multiple sources to be loaded using `CDATA`. **NOTE** this behavour is not documented but is present in GDAL test suite.


**IMPORTANT**: when using `/vsicurl/` it's necessary that streaming responses are disabled, GDAL needs the ´Content-length´ header to be present.

