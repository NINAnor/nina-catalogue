# import csv
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from django.db import transaction


def to_vrt(layername):
    root = ET.Element("OGRVRTDataSource")
    layer = ET.Element("OGRVRTLayer", attrib={"name": layername})
    root.append(layer)

    src_data_source = ET.Element("SrcDataSource")
    src_data_source.text = "{{SOURCE}}"
    layer.append(src_data_source)

    # field = ET.Element("Field", attrib={
    #     "src": "",
    #     "name": ""
    # })
    # layer.append(field)

    srs = ET.Element("LayerSRS")
    srs.text = "WGS84"
    layer.append(srs)

    geo_field = ET.Element(
        "GeometryField",
        attrib={
            "encoding": "PointFromColumns",
            "x": "decimalLongitude",
            "y": "decimalLatitude",
        },
    )
    layer.append(geo_field)
    geo_type = ET.Element("GeometryType")
    geo_type.text = "wkbPoint"
    geo_field.append(geo_type)

    return ET.tostring(root, encoding="utf-8").decode("utf-8")


def to_content(xml_path, dataset):
    meta_path = xml_path / "meta.xml"
    if not meta_path.is_file():
        raise Exception("There should be one meta.xml file")
    with open(str(meta_path)) as meta:
        soup = BeautifulSoup(meta, features="lxml-xml")
        with transaction.atomic():
            content = dataset.content

            data_file_path = xml_path / soup.find("location").text
            if not data_file_path.is_file():
                raise Exception(f"Missing file {data_file_path} declared in meta.xml")
            # with open(str(data_file_path)) as data_file:
            #     reader = csv.reader(data_file, delimiter='\t')
            #     for row in reader:
            #         headers = row
            #         break

            #     fields = {f['index']: f['term'].split('/')[-1] for f in soup.find_all('field')}
            #     fields[soup.find('id')['index']] = "id"
            content.gdal_vrt_definition = to_vrt(data_file_path.stem)
            content.remote_source = data_file_path.name
            content.save()
