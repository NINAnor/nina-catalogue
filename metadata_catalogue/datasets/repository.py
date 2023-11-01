# from pycsw.core.repository import Repository


class DatasetsRepository:
    """Class to interact with underlying repository"""

    def __init__(self, context, repo_filter=None):
        """Initialize repository"""

        self.context = context
        self.filter = repo_filter
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
        return []

        # identifiers are URN masked, where the last token of the identifier
        # is opendata.models.Resource.id (integer)
        # if ids are passed which are not int, silently return (does not exist)
        # try:
        #     return self._get_repo_filter(Resource.objects).filter(id__in=[s.split(':')[-1] for s in ids]).all()
        # except Exception as err:
        #     return []

    def query_domain(self, domain, typenames, domainquerytype="list", count=False):
        """Query by property domain values"""
        pass

        # objects = self._get_repo_filter(Resource.objects)

        # if domainquerytype == 'range':
        #     return [tuple(objects.aggregate(
        #     Min(domain), Max(domain)).values())]
        # else:
        #     if count:
        #         return [(d[domain], d['%s__count' % domain]) \
        #         for d in objects.values(domain).annotate(Count(domain))]
        #     else:
        #         return objects.values_list(domain).distinct()

    def query_insert(self, direction="max"):
        """Query to get latest (default) or earliest update to repository"""
        # from datetime import datetime
        # if direction == 'min':
        #     return Resource.objects.aggregate(
        #         Min('last_updated'))['last_updated__min'].strftime('%Y-%m-%dT%H:%M:%SZ')
        # return self._get_repo_filter(Resource.objects).aggregate(
        #     Max('last_updated'))['last_updated__max'].strftime('%Y-%m-%dT%H:%M:%SZ')

    def query_source(self, source):
        """Query by source"""
        # return self._get_repo_filter(Resource.objects).filter(source=source)

    def query(self, constraint, sortby=None, typenames=None, maxrecords=10, startposition=0):
        """Query records from underlying repository"""

        return [str(0), []]

        # # run the raw query and get total
        # if 'where' in constraint:  # GetRecords with constraint
        #     query = self._get_repo_filter(Resource.objects).extra(where=[constraint['where']], params=constraint['values'])

        # else:  # GetRecords sans constraint
        #     query = self._get_repo_filter(Resource.objects)

        # total = query.count()

        # # apply sorting, limit and offset
        # if sortby is not None:
        #     if 'spatial' in sortby and sortby['spatial']:  # spatial sort
        #         desc = False
        #         if sortby['order'] == 'DESC':
        #             desc = True
        #         query = query.all()
        #         return [str(total), sorted(query, key=lambda x: float(util.get_geometry_area(getattr(x, sortby['propertyname']))), reverse=desc)[startposition:startposition+int(maxrecords)]]
        #     if sortby['order'] == 'DESC':
        #         pname = '-%s' % sortby['propertyname']
        #     else:
        #         pname = sortby['propertyname']
        #     return [str(total), \
        #     query.order_by(pname)[startposition:startposition+int(maxrecords)]]
        # else:  # no sort
        #     return [str(total), query.all()[startposition:startposition+int(maxrecords)]]

    def _get_repo_filter(self, query):
        """Apply repository wide side filter / mask query"""
        return query
        # if self.filter is not None:
        #     return query.extra(where=[self.filter])
        # return query
