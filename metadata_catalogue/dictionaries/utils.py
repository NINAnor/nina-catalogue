from typing import Any, List

from rdflib import Literal, URIRef
from rdflib.plugins.sparql.evaluate import evalPart
from rdflib.plugins.sparql.evalutils import _eval
from rdflib.plugins.sparql.parserutils import CompValue
from rdflib.plugins.sparql.sparql import QueryContext, SPARQLError

from .conf import settings


def parse_accept_header(accept: str) -> list[str]:
    """
    Given an accept header string, return a list of media types in order of preference.

    :param accept: Accept header value
    :return: Ordered list of media type preferences
    """

    def _parse_preference(qpref: str) -> float:
        qparts = qpref.split("=")
        try:
            return float(qparts[1].strip())
        except (ValueError, IndexError):
            pass
        return 1.0

    preferences = []
    types = accept.split(",")
    dpref = 2.0
    for mtype in types:
        parts = mtype.split(";")
        parts = [part.strip() for part in parts]
        pref = dpref
        try:
            for part in parts[1:]:
                if part.startswith("q="):
                    pref = _parse_preference(part)
                    break
        except IndexError:
            pass
        # preserve order of appearance in the list
        dpref = dpref - 0.01
        preferences.append((parts[0], pref))
    preferences.sort(key=lambda x: -x[1])
    return [pref[0] for pref in preferences]


def eval_custom_functions(ctx: QueryContext, part: CompValue) -> list[Any]:
    """Retrieve variables from a SPARQL-query, then execute registered SPARQL functions
    The results are then stored in Literal objects and added to the query results.

    :param ctx:     <class 'rdflib.plugins.sparql.sparql.QueryContext'>
    :param part:    <class 'rdflib.plugins.sparql.parserutils.CompValue'>
    :return:        <class 'rdflib.plugins.sparql.processor.SPARQLResult'>
    """
    # This part holds basic implementation for adding new functions
    if part.name == "Extend":
        query_results: list[Any] = []
        # Information is retrieved and stored and passed through a generator
        for eval_part in evalPart(ctx, part.p):
            # Checks if the function is a URI (custom function)
            if hasattr(part.expr, "iri"):
                # Iterate through the custom functions passed in the constructor
                for function_uri, custom_function in settings.DICTIONARIES_FUNCTIONS.items():
                    # Check if URI correspond to a registered custom function
                    if part.expr.iri == URIRef(function_uri):
                        # Execute each function
                        query_results, ctx, part, _ = custom_function(query_results, ctx, part, eval_part)

            else:
                # For built-in SPARQL functions (that are not URIs)
                evaluation: list[Any] = [_eval(part.expr, eval_part.forget(ctx, _except=part._vars))]
                if isinstance(evaluation[0], SPARQLError):
                    raise evaluation[0]
                # Append results for built-in SPARQL functions
                for result in evaluation:
                    query_results.append(eval_part.merge({part.var: Literal(result)}))

        return query_results
    raise NotImplementedError()
