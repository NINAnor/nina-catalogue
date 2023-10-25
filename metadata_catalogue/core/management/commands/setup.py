from django.core.management import call_command
from django.core.management.base import BaseCommand

from metadata_catalogue.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.all().count() == 0:
            call_command("loaddata", "users.json")
        else:
            self.stdout.write("Users already present, ignoring")
