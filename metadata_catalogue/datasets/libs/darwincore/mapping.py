from bs4 import BeautifulSoup
from django.db import transaction
from django.template.loader import render_to_string

ROW_TYPES = {"http://rs.tdwg.org/dwc/terms/Event": "event", "http://rs.tdwg.org/dwc/terms/Occurrence": "occurrence"}


class SourceLayer:
    def __init__(self, node, base_path) -> None:
        if node["rowType"] not in ROW_TYPES:
            raise Exception(f"File implements a non supported row type: {node['rowType']}")

        self.type = ROW_TYPES[node["rowType"]]

        self.path = base_path / node.find("location").text
        if not self.path.is_file():
            raise Exception(f"Missing file {self.path} declared in meta.xml")

    def name(self):
        return self.path.name

    def __repr__(self) -> str:
        return f"{self.type} - {self.path.name}"


def to_content(xml_path, dataset):
    meta_path = xml_path / "meta.xml"
    if not meta_path.is_file():
        raise Exception("There should be one meta.xml file")
    with open(str(meta_path)) as meta:
        soup = BeautifulSoup(meta, features="lxml-xml")
        with transaction.atomic():
            content = dataset.content
            extensions = []
            core = SourceLayer(soup.find("core"), xml_path)
            for extension in soup.find_all("extension"):
                extensions.append(SourceLayer(extension, xml_path))

            # TODO: field mapping
            # with open(str(data_file_path)) as data_file:
            #     reader = csv.reader(data_file, delimiter='\t')
            #     for row in reader:
            #         headers = row
            #         break

            #     fields = {f['index']: f['term'].split('/')[-1] for f in soup.find_all('field')}
            #     fields[soup.find('id')['index']] = "id"

            ctx = {
                "core": core,
                "extensions": extensions,
                "source": dataset.fetch_url,
            }
            content.gdal_vrt_definition = render_to_string("vrt/occurrence.xml", ctx)
            content.save()
