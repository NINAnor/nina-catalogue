import json
import pathlib

from django.core.management.base import BaseCommand

from ...libs.imports import map_from_maplibre_style_spec


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("style_file", type=str, help="path to the style file")

    def handle(self, *args, **options):
        style_file = options.get("style_file")
        f = pathlib.Path(style_file)
        with open(str(f)) as file:
            style_dict = json.load(file)
            map_from_maplibre_style_spec(f.name, style_dict)
