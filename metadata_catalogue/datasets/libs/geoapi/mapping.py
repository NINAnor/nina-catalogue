class ResourceMapping:
    def __init__(self, dataset) -> None:
        self.id = dataset.uuid
        self.dataset = dataset

    def as_resource(self):
        return self.id, {
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
                    "name": "CSV",
                    "editable": False,
                }
            ],
        }
