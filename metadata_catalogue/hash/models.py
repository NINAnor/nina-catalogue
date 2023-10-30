from typing import Any

from django.db import models
from psqlextra.models import PostgresModel
from psqlextra.query import ConflictAction


class HashManager(models.Manager):
    def create(self, *args, **kwargs: Any) -> tuple[Any, bool]:
        return super().on_conflict(["hash"], ConflictAction.NOTHING).create(*args, **kwargs)


class HashedModel(PostgresModel):
    objects = HashManager()

    def save(self, *args, **kwargs):
        if self.id:
            raise Exception("Cannot update a hashed model")

        super().save(*args, **kwargs)

    def _do_insert(self, manager, using, fields, update_pk, raw):
        fields = [f for f in fields if f.attname not in ["hash"]]
        return super()._do_insert(manager, using, fields, update_pk, raw)

    class Meta:
        abstract = True
