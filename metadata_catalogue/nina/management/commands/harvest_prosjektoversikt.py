from django.core.management.base import BaseCommand

from ...libs.harvesters import prosjektoversikt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("url", type=str, help="projects api endpoint")
        parser.add_argument("--limit", type=int, help="how many lines to read at each request", default=50)

    def handle(self, *args, **options):
        url = options.get("url")
        limit = options.get("limit")
        prosjektoversikt(url, limit=limit)
