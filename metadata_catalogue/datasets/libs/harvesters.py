import logging
import pathlib
import tempfile
import traceback
import zipfile

import requests
from django.core.files.temp import NamedTemporaryFile

from metadata_catalogue.datasets.libs import darwincore, ipt
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
    print(dataset_id)
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        dataset.set_fetch_message("", success=False)

        if dataset.fetch_url:
            file = NamedTemporaryFile(delete=True)
            # TODO: handle network errors
            stream = requests.get(dataset.fetch_url, stream=True)
            for block in stream.iter_content(1024 * 8):
                if not block:
                    break
                file.write(block)

            file.flush()

            if dataset.fetch_type == Dataset.FetchType.DARWINCORE:
                try:
                    handle_file_as_darwincore_zip(file, dataset)
                    dataset.set_fetch_message("", append=True, success=True)
                except:
                    dataset.set_fetch_message(
                        traceback.format_exc(), append=True, logger_fn=logger.error, success=False
                    )
            else:
                dataset.set_fetch_message("Not implemented fetch type", logger_fn=logger.warn, success=False)
        else:
            dataset.set_fetch_message(
                f"No fetch URL for dataset {dataset_id}, ignoring", logger_fn=logger.warn, success=False
            )
    except Dataset.DoesNotExist:
        logger.error(f"No dataset found with id {dataset_id}")


def harvest_ipt(ipt_url):
    response = requests.get(f"{ipt_url}/rss")
    ipt.rss_to_datasets(response.text)
