import pathlib

from django.core.management.base import BaseCommand

from metadata_catalogue.datasets.libs import checks


class Command(BaseCommand):
    def handle(self, *args, **options):
        checks.vrt()
