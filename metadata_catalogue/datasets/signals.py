from django.db.models.signals import m2m_changed

from .models import Metadata


def update_xml_keyword(sender, instance, **kwargs):
    for m in instance.metadatas.all():
        m._update_xml(save=True)


m2m_changed.connect(update_xml_keyword, sender=Metadata.keywords.through)
