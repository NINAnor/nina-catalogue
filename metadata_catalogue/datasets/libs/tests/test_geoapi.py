import pytest
from django.contrib.gis.geos import Point, Polygon
from django.urls import reverse_lazy

from ...models import Dataset, Metadata
from ..geoapi.mapping import ResourceMapping

pytestmark = pytest.mark.django_db(transaction=True)


class TestPyGeoAPIResourceMapping:
    def setup_method(self):
        self.dataset = Dataset.objects.create(
            name="test",
            source="https://ipt.nina.no/resource?r=nina_artskart",
            fetch_url="https://ipt.nina.no/archive.do?r=nina_artskart",
            fetch_type=Dataset.FetchType.DARWINCORE,
        )

        bottom_left = Point(0, 0)
        top_right = Point(10, 10)

        rectangle = Polygon.from_bbox((bottom_left.x, bottom_left.y, top_right.x, top_right.y))
        rectangle.srid = 4326

        self.metadata = self.dataset.get_metadata()
        self.metadata.bounding_box = rectangle
        self.metadata.title = "test"
        self.metadata.abstract = "test"

        self.metadata.save()

    def test_mapping_to_pygeoapi_resource(self):
        id, rm = ResourceMapping(self.dataset, "http://testserver").as_resource()
        assert id == str(self.dataset.uuid)
        assert rm == {
            "type": "collection",
            "visibility": "default",
            "title": "test",
            "description": "test",
            "keywords": [],
            "context": [],
            "links": [
                {"type": "application/zip", "rel": "canonical", "title": "Data", "href": self.dataset.fetch_url}
            ],
            "extents": {
                "spatial": {
                    "bbox": (0.0, 0.0, 10.0, 10.0),
                    "crs": "WGS 84",
                }
            },
            "providers": [
                {
                    "type": "feature",
                    "default": True,
                    "name": "OGR",
                    "editable": False,
                    "id_field": "id",
                    "layer": "data",
                    "data": {
                        "source_type": "VRT",
                        "source_capabilities": {"paging": False},
                        "source": "/vsicurl/"
                        + "http://testserver"
                        + reverse_lazy("get-dataset-vrt", kwargs={"dataset_uuid": self.dataset.uuid}),
                    },
                }
            ],
        }
