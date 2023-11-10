# from pycsw.core.repository import Repository
from django.db.models import Max, Min

from metadata_catalogue.datasets.models import Dataset

from . import logger


class DatasetsRepository:
    """Class to interact with underlying repository"""

    def __init__(self, context, repo_filter=None):
        """Initialize repository"""

        self.context = context
        self.filter = repo_filter
        self.transactions = False
        self.dbtype = "postgresql+postgis+wkt"
        self.fts = False

        self.queryables = {}

        for tname in self.context.model["typenames"]:
            for qname in self.context.model["typenames"][tname]["queryables"]:
                self.queryables[qname] = {}

                for qkey, qvalue in self.context.model["typenames"][tname]["queryables"][qname].items():
                    self.queryables[qname][qkey] = qvalue

        # flatten all queryables
        # TODO smarter way of doing this
        self.queryables["_all"] = {}
        for qbl in self.queryables:
            self.queryables["_all"].update(self.queryables[qbl])
        self.queryables["_all"].update(self.context.md_core_model["mappings"])

    def query_ids(self, ids):
        """Query by list of identifiers"""
        return Dataset.objects.filter(uuid__in=ids).all().as_csw()

    def query_insert(self, direction="max"):
        """Query to get latest (default) or earliest update to repository"""
        if direction == "min":
            return Dataset.objects.aggregate(Min("last_modified_at"))["last_modified_at__min"].strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        return Dataset.objects.aggregate(Max("last_modified_at"))["last_modified_at__max"].strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

    def query_source(self, source):
        """Query by source"""
        return Dataset.objects.filter(source=source)

    def query(self, constraint, sortby=None, typenames=None, maxrecords=10, startposition=0):
        """Query records from underlying repository"""
        limit = int(maxrecords)
        offset = int(startposition)
        query = Dataset.objects.csw_filter(constraint)
        if sortby:
            query = query.csw_sort(sortby)
        return [str(query.count()), query[offset : offset + limit].as_csw()]
