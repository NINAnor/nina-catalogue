import pathlib

from django.core.management.base import BaseCommand

from metadata_catalogue.datasets.models import Dataset


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("folder", type=str, help="folder to populate with vrt", default="vrts")

    def handle(self, *args, **options):
        dts = Dataset.objects.select_related("content").all()

        f = pathlib.Path(options.get("folder"))
        f.mkdir(exist_ok=True)

        for dt in dts:
            (f / f"{str(dt.uuid)}.vrt").write_text(dt.content.gdal_vrt_definition, encoding="utf-8")

        print("You now can go to the created folder and run \"ls | args -L 1 -d '\n' ogrinfo\"")
