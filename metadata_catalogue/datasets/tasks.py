from procrastinate.contrib.django import app
from metadata_catalogue.datasets.libs.harvesters import harvest_ipt, harvest_dataset
from metadata_catalogue.datasets.libs.checks import validate_vrt

from django.conf import settings
import logging


@app.periodic(cron=settings.IPT_SOURCES_CRON)
@app.task(name="harvest_ipt")
def harvest_ipt_task(timestamp: int):
    for url in settings.IPT_SOURCES:
        logging.info(f"fetching {url}")
        harvest_ipt(ipt_url=url)


@app.task(name="harvest_dataset")
def harvest_dataset_task(dataset_id: int):
    harvest_dataset(dataset_id=dataset_id)


@app.task(name="validate_vrt")
def validate_vrt_task(content_id):
    validate_vrt(content_id=content_id)
