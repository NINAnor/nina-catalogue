from django.core.management.base import BaseCommand

from metadata_catalogue.datasets.libs.harvester import harvest_dataset


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("dataset_id", type=int, help="id of the dataset")

    def handle(self, *args, **options):
        dataset_id = options.get("dataset_id")
        harvest_dataset(dataset_id)
