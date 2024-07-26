import pathlib
import re

from bs4 import BeautifulSoup
from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string


class SourceLayer:
    def __init__(self, node, base_path, extension=False) -> None:
        self.type = pathlib.Path(node.find("location").text).stem

        self.path = base_path / node.find("location").text
        if not self.path.is_file():
            raise Exception(f"Missing file {self.path} declared in meta.xml")

        with open(str(self.path), encoding=node["encoding"]) as f:
            sep = re.compile(node["fieldsTerminatedBy"])
            headers = re.split(sep, f.readline().rstrip())

            # extensions nodes have a "coreid" fields that contains the id of "core" row, this is needed for the join
            id_field_lookup = "coreid" if extension else "id"
            self.id = headers[int(node.find(id_field_lookup)["index"])]

            # TODO: field mapping if necessary

    def __str__(self) -> str:
        return self.type


def to_content(xml_path, dataset):
    meta_path = xml_path / "meta.xml"
    if not meta_path.is_file():
        raise Exception("There should be one meta.xml file")
    with open(str(meta_path)) as meta:
        soup = BeautifulSoup(meta, features="lxml-xml")
        with transaction.atomic():
            content = dataset.get_content()
            extensions = []
            core = SourceLayer(soup.find("core"), xml_path)
            for extension in soup.find_all("extension"):
                extensions.append(SourceLayer(extension, xml_path, extension=True))

            geometry_field = None
            for _wkt in soup.findAll("field", {"term": "http://rs.tdwg.org/dwc/terms/footprintWKT"}):
                geometry_field = "footprintWKT"
                break

            ctx = {
                "core": core,
                "extensions": extensions,
                "source": dataset.fetch_url,
                "layer_name": settings.GEOAPI_DWCA_LAYER_NAME,
                "geometry_field": geometry_field,
            }
            content.gdal_vrt_definition = render_to_string("vrt/definition.xml", ctx)
            content.save()
