from django.core.management.base import BaseCommand

from metadata_catalogue.datasets.libs.iso.regenerate import regenerate_xml


class Command(BaseCommand):
    def handle(self, *args, **options):
        regenerate_xml()
