from ...models import Metadata


def regenerate_xml():
    for meta in Metadata.objects.all():
        meta._update_xml(save=True)
