from django.contrib.gis.db import models

from . import logger
from .libs.csw_mapping import CSWMapping
from .libs.csw_query import Group

SORT_CONFIG = {"title": "metadata__title", "csw_wkt_geometry": "metadata__bounding_box"}


class DatasetQuerySet(models.QuerySet):
    def as_csw(self, *args, warn=True, **kwargs):
        logger.warn("DANGER: This method consumes the queryset and returns and array of items")
        return [CSWMapping(instance) for instance in self]

    def csw_filter(self, filter):
        if not filter:
            return self

        if "ogc:Filter" in filter["_dict"]:
            if filter_group := Group(filter["_dict"]["ogc:Filter"]):
                q = self.filter(filter_group.to_q())
                logger.debug(q.query)
                return q
        return self

    def csw_sort(self, sort):
        try:
            return self.order_by(f'{"-" if sort["order"] == "DESC" else ""}{SORT_CONFIG[sort["propertyname"]]}')
        except (AttributeError, KeyError):
            logger.warn(f"Not implemented! {sort}")
        return self


class DatasetManager(models.Manager):
    def get_queryset(self):
        return DatasetQuerySet(self.model, using=self._db)

    def as_csw(self, *args, **kwargs):
        return self.get_queryset().as_csw(*args, **kwargs)

    def csw_filter(self, *args, **kwargs):
        return self.get_queryset().csw_filter(*args, **kwargs)
