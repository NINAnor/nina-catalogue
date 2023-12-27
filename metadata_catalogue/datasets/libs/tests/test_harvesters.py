from unittest.mock import patch

import pytest

from ...models import Dataset
from ..harvesters import handle_file_as_darwincore_zip, harvest_dataset

pytestmark = pytest.mark.django_db(transaction=True)
from django.core.management import call_command

TEST_DATA_FILES_PATH = "metadata_catalogue/datasets/libs/tests/data"


class TestHarvestDatabase:
    def setup_method(self):
        self.dataset = Dataset.objects.create(
            name="test",
            source="https://ipt.nina.no/resource?r=nina_artskart",
            fetch_url="https://ipt.nina.no/archive.do?r=nina_artskart",
            fetch_type=Dataset.FetchType.DARWINCORE,
        )

    @patch("metadata_catalogue.datasets.libs.harvesters.handle_file_as_darwincore_zip")
    def test_fetch_dataset(
        self,
        mock,
    ):
        harvest_dataset(self.dataset.id)
        assert mock.called

    @patch("metadata_catalogue.datasets.libs.harvesters.darwincore.to_metadata")
    @patch("metadata_catalogue.datasets.libs.harvesters.darwincore.to_content")
    def test_handle_darwincore_zip(self, m1, m2):
        handle_file_as_darwincore_zip(open(f"{TEST_DATA_FILES_PATH}/dwca_mini.zip"), self.dataset)
        assert m1.called
        assert m2.called

    @patch("metadata_catalogue.datasets.libs.harvesters.darwincore.to_metadata")
    @patch("metadata_catalogue.datasets.libs.harvesters.darwincore.to_content")
    def test_handle_darwincore_zip_no_eml(self, m1, m2):
        with pytest.raises(Exception):
            handle_file_as_darwincore_zip(open(f"{TEST_DATA_FILES_PATH}/dwca_no_eml.zip"), self.dataset)
        assert not m1.called
        assert not m2.called
