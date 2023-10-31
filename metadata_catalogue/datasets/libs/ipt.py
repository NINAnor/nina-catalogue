import logging
import traceback

from bs4 import BeautifulSoup
from django.db import transaction
from django_q.tasks import async_task

logger = logging.getLogger(__name__)

from metadata_catalogue.datasets.models import Dataset


def rss_to_datasets(rss_content):
    soup = BeautifulSoup(rss_content, features="lxml-xml")
    with transaction.atomic():
        for item in soup.find_all("item"):
            try:
                archive = item.find("ipt:dwca")
                if archive:
                    d, _ = Dataset.objects.update_or_create(
                        defaults={"name": item.find("title").text, "fetch_type": Dataset.FetchType.DARWINCORE},
                        fetch_url=archive.text,
                    )
                    async_task("metadata_catalogue.datasets.libs.harvesters.harvest_dataset", d.id)
                else:
                    logger.warn(f'no archive url found for {item.find("title").text}')
            except Exception:
                logger.error(traceback.format_exc())
