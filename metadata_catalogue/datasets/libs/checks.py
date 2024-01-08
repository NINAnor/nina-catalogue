import logging
import traceback

from django.apps import apps
from osgeo import gdal


def check_definition(content):
    vrt_mem_file = "/vsimem/input.vrt"
    gdal.FileFromMemBuffer(vrt_mem_file, bytes(content.gdal_vrt_definition, "utf-8"))
    # Create a virtual in-memory file for the GeoJSON output
    geojson_mem_file = "/vsimem/output.geojson"

    # Convert VRT to GeoJSON
    options = gdal.VectorTranslateOptions(format="GeoJSON")
    gdal.VectorTranslate(geojson_mem_file, vrt_mem_file, options=options)


def vrt():
    Dataset = apps.get_model("datasets", "Dataset")
    dts = Dataset.objects.select_related("content").all()

    for dt in dts:
        try:
            check_definition(dt.content)
        except:
            logging.warn(f"{dt.fetch_url}{traceback.format_exc()}")


def validate_vrt(content_id):
    Content = apps.get_model("datasets", "Content")
    content = Content.objects.get(id=content_id)
    try:
        check_definition(content)
        content.valid = True
    except:
        logging.error(f"VRT ERROR: {content.dataset_id} - {traceback.format_exc()}")
        content.valid = False
    content.save(update_fields=["valid"])
