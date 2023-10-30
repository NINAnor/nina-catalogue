from django.db.models.signals import post_save
from django.dispatch import receiver

from metadata_catalogue.datasets.models import Dataset, Metadata


@receiver(post_save, sender=Dataset)
def create_favorites(sender, instance, created, **kwargs):
    if created:
        Metadata.objects.create(dataset=instance)

    # TODO: run fetching in queue
