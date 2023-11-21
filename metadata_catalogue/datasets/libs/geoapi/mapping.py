from django.conf import settings
from django.urls import reverse_lazy


class ResourceMapping:
    def __init__(self, dataset, base_name) -> None:
        self.id = dataset.uuid
        self.dataset = dataset
        self.base_name = base_name

    def as_resource(self):
        return str(self.id), {
            "type": "collection",
            "visibility": "default",
            "title": self.dataset.metadata.title,
            "description": self.dataset.metadata.abstract,
            "keywords": [],
            "context": [],
            "links": [
                {"type": "application/zip", "rel": "canonical", "title": "Data", "href": self.dataset.fetch_url}
            ],
            "extents": {
                "spatial": {
                    "bbox": self.dataset.metadata.bounding_box.extent,
                    "crs": self.dataset.metadata.bounding_box.srs.name,
                }
            },
            "providers": [
                {
                    "type": "feature",
                    "default": True,
                    "name": "OGR",
                    "editable": False,
                    "id_field": "id",
                    "layer": settings.GEOAPI_DWCA_LAYER_NAME,
                    "data": {
                        "source_type": "VRT",
                        "source": "/vsicurl/"
                        + self.base_name
                        + reverse_lazy("get-dataset-vrt", kwargs={"dataset_uuid": self.dataset.uuid}),
                    },
                }
            ],
        }
