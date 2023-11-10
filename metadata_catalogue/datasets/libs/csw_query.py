import operator
from functools import reduce

import pyproj
from django.contrib.gis.geos import Polygon
from django.db.models import Q

from .. import logger


def bbox_to_geometry(bbox):
    xmin, ymin = bbox["gml:lowerCorner"].split(" ")
    xmax, ymax = bbox["gml:upperCorner"].split(" ")
    p = Polygon.from_bbox((xmin, ymin, xmax, ymax))
    if "@srsName" in bbox:
        p.srid = pyproj.CRS.from_string(bbox["@srsName"]).to_epsg()
    else:
        p.srid = 4326
    return p


def not_implemented_search(r):
    return Q()


class Rule:
    def __init__(self, operation, ogc_dict):
        _prefix, self.operation = operation.split(":")
        self._dict = ogc_dict
        _prefix, self.field = ogc_dict["ogc:PropertyName"].split(":")
        self._get_value()

    def _get_value(self):
        if self.operation == "BBOX":
            self.value = bbox_to_geometry(self._dict["gml:Envelope"])
        else:
            self.value = self._dict["ogc:Literal"]

    IMPLEMENTATION = {
        "PropertyIsLike": {
            "AnyText": lambda r: Q(metadata__fts__icontains=r.value),
            "ServiceType": lambda r: Q() if r.value == "view" else Q(id__lt=0),
        },
        "BBOX": {
            "BoundingBox": lambda r: Q(metadata__bounding_box__within=r.value),
        },
    }

    def to_q(self):
        try:
            return self.IMPLEMENTATION[self.operation][self.field](self)
        except KeyError:
            logger.warn(f"Not implemented! {self.field} {self.operation} {self.value}")
        return Q()


class Group:
    def __init__(self, xml) -> None:
        self.rules = []
        self.combinator = operator.and_

        for k, v in xml.items():
            if k in ["ogc:And", "ogc:Or"]:
                self.combinator = operator.or_ if k == "ogc:Or" else operator.and_
                if isinstance(v, list):
                    [self.rules.append(Group(subvalue)) for subvalue in v]
                else:
                    self.rules.append(Group(v))
            else:
                if isinstance(v, list):
                    [self.rules.append(Rule(k, subvalue)) for subvalue in v]
                else:
                    self.rules.append(Rule(k, v))

    def to_q(self):
        rules = [rule.to_q() for rule in self.rules]
        return reduce(self.combinator, rules) if len(rules) > 1 else rules[0]
