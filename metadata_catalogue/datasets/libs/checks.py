import traceback

from osgeo import gdal

from metadata_catalogue.datasets.models import Dataset


def vrt():
    dts = Dataset.objects.select_related("content").all()
    vrt_mem_file = "/vsimem/input.vrt"

    for dt in dts:
        try:
            gdal.FileFromMemBuffer(vrt_mem_file, bytes(dt.content.gdal_vrt_definition, "utf-8"))
            # Create a virtual in-memory file for the GeoJSON output
            geojson_mem_file = "/vsimem/output.geojson"

            # Convert VRT to GeoJSON
            options = gdal.VectorTranslateOptions(format="GeoJSON")
            gdal.VectorTranslate(geojson_mem_file, vrt_mem_file, options=options)
        except:
            print(dt.fetch_url)
            print(traceback.format_exception())
