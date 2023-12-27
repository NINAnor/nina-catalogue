from unittest.mock import patch

import pytest
from languages_plus.models import Language

from metadata_catalogue.datasets.models import Content, Dataset, Keyword, Metadata

pytestmark = pytest.mark.django_db


class TestDatasetModel:
    def test_dataset_related_object_access_raise_exception(self):
        d = Dataset.objects.create(name="test")

        with pytest.raises(Dataset.metadata.RelatedObjectDoesNotExist):
            d.metadata

        with pytest.raises(Dataset.content.RelatedObjectDoesNotExist):
            d.content

    def test_dataset_no_raise_exception(self):
        d = Dataset.objects.create(name="test")
        m = d.get_metadata()
        assert m.id is not None
        assert type(m) == Metadata
        c = d.get_content()
        assert c.id is not None
        assert type(c) == Content

        assert d.metadata
        assert d.content


class TestMetadataModel:
    @patch.object(Metadata, "_update_xml")
    def test_watch_update(self, mock):
        d = Dataset.objects.create(name="test")
        m = d.get_metadata()
        assert m.xml == ""
        m.title = "test"
        m.abstract = "test"
        m.language, _ = Language.objects.get_or_create(iso_639_1="en")
        m.source = "http://nina.no"
        m.bounding_box = None
        m.geographic_description = "Somewhere"
        m.save()
        assert mock.called

    @patch.object(Metadata, "_update_xml")
    def test_watch_update_m2m(self, mock):
        d = Dataset.objects.create(name="test")
        m = d.get_metadata()
        k = Keyword.objects.create(name="test")
        m.keywords.add(k)
        assert mock.called


class TestContentModel:
    @patch("metadata_catalogue.datasets.models.async_task")
    def test_watch_update(self, mock):
        d = Dataset.objects.create(name="test")
        c = d.get_content()
        c.gdal_vrt_definition = "test, this is invalid"
        c.save()
        assert mock.called
