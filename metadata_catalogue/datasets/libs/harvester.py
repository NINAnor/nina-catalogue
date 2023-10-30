import logging
import pathlib
import tempfile
import zipfile

import requests
from django.core.files.temp import NamedTemporaryFile

from metadata_catalogue.datasets.libs import darwincore
from metadata_catalogue.datasets.models import Dataset

logger = logging.getLogger(__name__)


def handle_file_as_darwincore_zip(file: NamedTemporaryFile, dataset: Dataset):
    zf = zipfile.ZipFile(file.name)

    with tempfile.TemporaryDirectory() as tempdir:
        zf.extractall(tempdir)
        path = pathlib.Path(tempdir)
        eml = path / "eml.xml"
        if not eml.is_file():
            raise Exception("There should be one eml.xml file")

        darwincore.to_metadata(eml, dataset)


def harvest_dataset(dataset_id: int):
    try:
        dataset = Dataset.objects.get(id=dataset_id)

        if dataset.fetch_url:
            file = NamedTemporaryFile(delete=True)
            stream = requests.get(dataset.fetch_url, stream=True)
            for block in stream.iter_content(1024 * 8):
                if not block:
                    break
                file.write(block)

            file.flush()

            if dataset.fetch_type == Dataset.FetchType.DARWINCORE:
                handle_file_as_darwincore_zip(file, dataset)
            else:
                raise Exception("Not implemented fetch type")
        else:
            logger.warn(f"No fetch URL for dataset {dataset_id}, ignoring")
    except Dataset.DoesNotExist:
        logger.error(f"No dataset found with id {dataset_id}")
