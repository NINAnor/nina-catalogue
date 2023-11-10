import operator
import re
from functools import reduce

import pyproj
from django.contrib.gis.geos import LinearRing, Polygon
from django.db.models import Q

from .. import logger


def set_srid(gml_dict, geom):
    if "@srsName" in gml_dict:
        geom.srid = pyproj.CRS.from_string(gml_dict["@srsName"]).to_epsg()
    else:
        geom.srid = 4326


def build_linear_ring(ring):
    coords = [float(coord) for coord in ring["gml:posList"]["#text"].split(" ")]
    dimension = int(ring["gml:posList"]["@srsDimension"])
    tuples = [tuple(coords[i * dimension : (i + 1) * dimension]) for i in range(int(len(coords) / dimension))]
    return LinearRing(*tuples)


def to_sql_like_regex(term):
    escaped = re.escape(term)
    return re.compile(escaped.replace(r"\?", ".").replace(r"\%", ".*"))


class Rule:
    def __init__(self, operation, ogc_dict):
        _prefix, self.operation = operation.split(":")
        self._dict = ogc_dict
        self.function = None
        self.field = None
        if "ogc:Function" in self._dict:
            # TODO: implement functions
            self.function = self._dict["ogc:Function"]["@name"]
            _prefix, self.field = self._dict["ogc:Function"]["ogc:PropertyName"].split(":")
        elif "ogc:PropertyName" in self._dict:
            _prefix, self.field = self._dict["ogc:PropertyName"].split(":")
        self._get_value()

    def _get_value(self):
        if "gml:Envelope" in self._dict:
            bbox = self._dict["gml:Envelope"]
            xmin, ymin = bbox["gml:lowerCorner"].split(" ")
            xmax, ymax = bbox["gml:upperCorner"].split(" ")
            self.value = Polygon.from_bbox((xmin, ymin, xmax, ymax))
            set_srid(bbox, self.value)
        elif "gml:Polygon" in self._dict:
            polygon = self._dict["gml:Polygon"]
            # TODO: manage interior rings for polygon
            self.value = Polygon(build_linear_ring(polygon["gml:exterior"]["gml:LinearRing"]))
            set_srid(polygon, self.value)

        elif "ogc:Literal" in self._dict:
            self.value = self._dict["ogc:Literal"]
        else:
            self.value = None

    IMPLEMENTATION = {
        "PropertyIsLike": {
            "AnyText": lambda r: Q(metadata__fts__iregex=to_sql_like_regex(r.value)),
            "Abstract": lambda r: Q(metadata__abstract__iregex=to_sql_like_regex(r.value)),
            "Title": lambda r: Q(metadata__title__iregex=to_sql_like_regex(r.value)),
            "ServiceType": lambda r: Q() if r.value == "view" else Q(id__lt=0),
        },
        "BBOX": {
            "BoundingBox": lambda r: Q(metadata__bounding_box__within=r.value),
        },
        "PropertyIsBetween": {
            "title": lambda r: Q(
                metadata__title__lt=r._dict["ogc:UpperBoundary"]["ogc:Literal"],
                metadata__title__gt=r._dict["ogc:LowerBoundary"]["ogc:Literal"],
            ),
        },
    }

    def __repr__(self) -> str:
        return f"\n\t({self.operation} {self.field} {self.value if self.value else ''})"

    def to_q(self):
        try:
            return self.IMPLEMENTATION[self.operation][self.field](self)
        except KeyError:
            logger.warn(f"Not implemented! {self.field} {self.operation} {self.value}")
        return Q()


COMBINATORS = {
    "ogc:And": operator.and_,
    "ogc:Or": operator.or_,
    "ogc:Not": operator.not_,
}
REVERSED = {v: k for k, v in COMBINATORS.items()}


class Group:
    def __init__(self, xml, combinator=None) -> None:
        self.rules = []
        self.combinator = combinator

        for k, v in xml.items():
            if k in COMBINATORS.keys():
                if isinstance(v, list):
                    [self.rules.append(Group(subvalue, COMBINATORS[k])) for subvalue in v]
                else:
                    self.rules.append(Group(v, COMBINATORS[k]))
            else:
                if isinstance(v, list):
                    [self.rules.append(Rule(k, subvalue)) for subvalue in v]
                else:
                    self.rules.append(Rule(k, v))

    def __repr__(self) -> str:
        return f"{REVERSED[self.combinator] if self.combinator else ''}{self.rules}"

    def to_q(self):
        if self.combinator == operator.not_:
            return ~(self.rules[0].to_q())
        if len(self.rules) == 1:
            return self.rules[0].to_q()
        if not self.combinator and len(self.rules) > 1:
            raise Exception("multiple rules detected without a combinator")
        else:
            return reduce(self.combinator, [rule.to_q() for rule in self.rules])
