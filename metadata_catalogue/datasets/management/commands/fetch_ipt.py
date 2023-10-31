from django.core.management.base import BaseCommand

from metadata_catalogue.datasets.libs.harvesters import harvest_ipt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ipt_base_url", type=str, help="url of the ipt resource")

    def handle(self, *args, **options):
        ipt_url = options.get("ipt_base_url")
        harvest_ipt(ipt_url)
