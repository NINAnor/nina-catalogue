import collections
import operator

from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from django.db.models import Q

from metadata_catalogue.datasets.libs.csw_mapping import CSWMapping

from . import logger


def bbox_to_geometry(bbox):
    xmin, ymin = bbox["gml:lowerCorner"].split(" ")
    xmax, ymax = bbox["gml:upperCorner"].split(" ")
    p = Polygon.from_bbox((xmin, ymin, xmax, ymax))
    p.srid = 4326
    logger.info(p.ewkt)
    return p


OGC_TO_Q = {
    "ogc:PropertyIsLike": {"csw:AnyText": lambda ogc_dict: Q(metadata__fts__icontains=ogc_dict["ogc:Literal"])},
    "ogc:BBOX": {
        "ows:BoundingBox": lambda ogc_dict: Q(
            metadata__bounding_box__within=bbox_to_geometry(ogc_dict["gml:Envelope"])
        ),
        "apiso:BoundingBox": lambda ogc_dict: Q(
            metadata__bounding_box__within=bbox_to_geometry(ogc_dict["gml:Envelope"])
        ),
    },
}


def with_boolean_operators(filter, op=operator.and_):
    q = Q()

    print(filter)
    for query in OGC_TO_Q.keys():
        if query in filter and filter[query]["ogc:PropertyName"]:
            result = OGC_TO_Q[query][filter[query]["ogc:PropertyName"]](filter[query])
            q = op(q, result)

    return q


OPERATORS = collections.defaultdict(lambda _: operator.and_)
OPERATORS["ogc:Or"] = operator.or_
OPERATORS["ogc:And"] = operator.and_


def ogc_filter_to_q(filter):
    op = "ogc:And"
    query = filter
    if any(k in filter for k in OPERATORS.keys()):
        print("has an operator")
        for k in OPERATORS.keys():
            if k in filter:
                query = filter[k]
                op = k
                break

    return with_boolean_operators(query, op=OPERATORS[op])


class DatasetQuerySet(models.QuerySet):
    def as_csw(self, *args, warn=True, **kwargs):
        logger.warn("DANGER: This method consumes the queryset and returns and array of items")
        return [CSWMapping(instance) for instance in self]

    def csw_filter(self, filter):
        if not filter:
            return self

        if "ogc:Filter" in filter["_dict"]:
            if filter := ogc_filter_to_q(filter["_dict"]["ogc:Filter"]):
                q = self.filter(filter)
                print(q.query)
                return q
        return self


class DatasetManager(models.Manager):
    def get_queryset(self):
        return DatasetQuerySet(self.model, using=self._db)

    def as_csw(self, *args, **kwargs):
        return self.get_queryset().as_csw(*args, **kwargs)

    def csw_filter(self, *args, **kwargs):
        return self.get_queryset().csw_filter(*args, **kwargs)
