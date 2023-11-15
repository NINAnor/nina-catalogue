import traceback

from countries_plus.models import Country
from django.core.management import call_command
from django.core.management.base import BaseCommand
from languages_plus.models import Language

from metadata_catalogue.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.all().first() is None:
            call_command("loaddata", "users.json")

        if Country.objects.all().first() is None:
            try:
                call_command("update_countries_plus")
            except:
                print(traceback.format_exc())
                print("Falling back to local fixture")
            call_command("loaddata", "countries.json.gz")

        if Language.objects.all().first() is None:
            call_command("loaddata", "languages_data.json.gz")
