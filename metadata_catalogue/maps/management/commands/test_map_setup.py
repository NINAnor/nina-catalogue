from django.core.management import call_command
from django.core.management.base import BaseCommand

from metadata_catalogue.maps.models import PortalMap


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not PortalMap.objects.all().exists():
            call_command("loaddata", "maps.json")
