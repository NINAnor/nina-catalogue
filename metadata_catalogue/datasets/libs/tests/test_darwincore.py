from pathlib import Path
from unittest.mock import patch

import pytest
from django.core.management import call_command

from ...models import Dataset, Keyword, License
from ..darwincore import deserializer, mapping

pytestmark = pytest.mark.django_db(transaction=True)
TEST_DATA_FILES_PATH = "metadata_catalogue/datasets/libs/tests/data"


class TestEMLToMetadata:
    def setup_method(self):
        call_command("setup")
        self.dataset = Dataset.objects.create(name="test")
        self.metadata = self.dataset.get_metadata()

    def test_metadata_import_from_eml(self):
        deserializer.to_metadata(TEST_DATA_FILES_PATH + "/eml.xml", self.dataset)
        assert self.metadata.title == "NINA test eml"
        assert Keyword.objects.count() == 2
        assert License.objects.count() == 1
        assert self.metadata.bounding_box.srid == 4326
        assert self.metadata.bounding_box.extent == (10, 10, 10, 10)


class TestDWCAToVRT:
    def setup_method(self):
        self.dataset = Dataset.objects.create(name="test", fetch_url="http://test")
        self.content = self.dataset.get_content()

    @patch("metadata_catalogue.datasets.models.async_task")
    def test_mapping_vrt_occurrence(self, mock):
        TEST_FOLDERS = ["/dwca_simple", "/dwca_measurements", "/dwca_wkt"]
        for test_folder in TEST_FOLDERS:
            test_path = Path(TEST_DATA_FILES_PATH + test_folder)
            mapping.to_content(test_path, self.dataset)
            assert mock.called
            assert self.content.gdal_vrt_definition != ""
            # TODO: assert the content is as expected

        with pytest.raises(Exception) as e:
            test_path = Path(TEST_DATA_FILES_PATH + "/dwca_missing_file")
            mapping.to_content(test_path, self.dataset)
            assert str(e) == f"Missing file {str(test_path / 'occurrence.txt')} declared in meta.xml"

        with pytest.raises(Exception) as e:
            test_path = Path(TEST_DATA_FILES_PATH + "/dwca_missing_meta")
            mapping.to_content(test_path, self.dataset)
            assert str(e) == "There should be one meta.xml file"
