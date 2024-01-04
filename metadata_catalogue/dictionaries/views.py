# Code based on rdflib-entrypoint
# the original code has bindings only for fastapi
# this aims to provide a sparql endpoint over rdflib-django3 stored graph
# See: https://github.com/vemonet/rdflib-endpoint/blob/main/src/rdflib_endpoint/sparql_router.py

import logging
import re
from typing import Any
from urllib import parse

import rdflib
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rdflib import RDF, Graph, URIRef
from rdflib.plugins.sparql import prepareQuery, prepareUpdate
from rdflib_django.utils import get_conjunctive_graph

from .conf import settings
from .utils import eval_custom_functions, parse_accept_header


class SPARQLView(View):
    @csrf_exempt
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if settings.DICTIONARIES_CUSTOM_EVAL:
            rdflib.plugins.sparql.CUSTOM_EVALS["evalCustomFunctions"] = settings.DICTIONARIES_CUSTOM_EVAL
        elif len(settings.DICTIONARIES_FUNCTIONS) > 0:
            rdflib.plugins.sparql.CUSTOM_EVALS["evalCustomFunctions"] = eval_custom_functions

        self.graph = get_conjunctive_graph()
        return super().dispatch(request, *args, **kwargs)

    def _handle_sparql_request(
        self, request: HttpRequest, query: str | None = None, update: str | None = None
    ) -> HttpResponse:
        """Handle SPARQL requests to the GET and POST endpoints"""
        if query and update:
            return JsonResponse(
                status=400,
                data={"message": "Cannot do both query and update"},
            )

        if not query and not update:
            accept = str(request.headers.get("accept", ""))
            if accept.startswith("text/html"):
                return render(
                    request,
                    template_name="dictionaries/yasgui.html",
                    context={
                        "title": settings.DICTIONARIES_DEFAULT_TITLE,
                        "description": settings.DICTIONARIES_DEFAULT_DESCRIPTION,
                        "example_query": settings.DICTIONARIES_DEFAULT_EXAMPLE,
                        "example_queries": settings.DICTIONARIES_EXAMPLE_QUERIES,
                    },
                )

            # If not asking HTML, return the SPARQL endpoint service description
            service_graph = self._get_service_graph()

            # Return the service description RDF as turtle or XML
            if accept == "text/turtle":
                return HttpResponse(
                    service_graph.serialize(format="turtle"),
                    headers={"content-type": "text/turtle"},
                )
            else:
                return HttpResponse(
                    service_graph.serialize(format="xml"),
                    headers={"content-type": "application/xml"},
                )

        # Pretty print the query object
        # from rdflib.plugins.sparql.algebra import pprintAlgebra
        # parsed_query = parser.parseQuery(query)
        # tq = algebraTranslateQuery(parsed_query)
        # pprintAlgebra(tq)

        graph_ns = dict(self.graph.namespaces())

        if query:
            try:
                parsed_query = prepareQuery(query, initNs=graph_ns)
                query_results = self.graph.query(parsed_query, processor=settings.DICTIONARIES_PROCESSOR)

                # Format and return results depending on Accept mime type in request header
                mime_types = parse_accept_header(
                    request.headers.get("accept", settings.DICTIONARIES_DEFAULT_CONTENT_TYPE)
                )

                # Handle cases that are more complicated, like it includes multiple
                # types, extra information, etc.
                output_mime_type = settings.DICTIONARIES_DEFAULT_CONTENT_TYPE
                for mime_type in mime_types:
                    if mime_type in settings.DICTIONARIES_CONTENT_TYPE_TO_RDFLIB_FORMAT:
                        output_mime_type = mime_type
                        # Use the first mime_type that matches
                        break

                query_operation = re.sub(r"(\w)([A-Z])", r"\1 \2", parsed_query.algebra.name)

                # Handle mime type for construct queries
                if query_operation == "Construct Query":
                    if output_mime_type in {"application/json", "text/csv"}:
                        output_mime_type = "text/turtle"
                        # TODO: support JSON-LD for construct query?
                        # g.serialize(format='json-ld', indent=4)
                    elif output_mime_type == "application/xml":
                        output_mime_type = "application/rdf+xml"
                    else:
                        pass  # TODO what happens here?

                try:
                    rdflib_format = settings.DICTIONARIES_CONTENT_TYPE_TO_RDFLIB_FORMAT[output_mime_type]
                    headers = {"content-type": output_mime_type}
                    response = HttpResponse(
                        query_results.serialize(format=rdflib_format),
                        headers=headers,
                    )
                except Exception as e:
                    logging.error(f"Error serializing the SPARQL query results with RDFLib: {e}")
                    return JsonResponse(
                        status=422,
                        data={"message": f"Error serializing the SPARQL query results with RDFLib: {e}"},
                    )
                else:
                    return response
            except Exception as e:
                logging.error(f"Error executing the SPARQL query on the RDFLib Graph: {e}")
                return JsonResponse(
                    status=400,
                    data={"message": f"Error executing the SPARQL query on the RDFLib Graph: {e}"},
                )
        else:  # Update
            if not settings.DICTIONARIES_ENABLE_UPDATE:
                return JsonResponse(status=403, data={"message": "INSERT and DELETE queries are not allowed."})
            if rdflib_apikey := settings.DICTIONARIES_RDFLIB_APIKEY:
                authorized = False
                if auth_header := request.headers.get("Authorization"):  # noqa: SIM102
                    if auth_header.startswith("Bearer ") and auth_header[7:] == rdflib_apikey:
                        authorized = True
                if not authorized:
                    return JsonResponse(status=403, data={"message": "Invalid API KEY."})
            try:
                prechecked_update: str = update  # type: ignore
                parsed_update = prepareUpdate(prechecked_update, initNs=graph_ns)
                self.graph.update(parsed_update, "sparql")
                return HttpResponse(status=204)
            except Exception as e:
                logging.error(f"Error executing the SPARQL update on the RDFLib Graph: {e}")
                return JsonResponse(
                    status=400,
                    data={"message": f"Error executing the SPARQL update on the RDFLib Graph: {e}"},
                )

    def _get_service_graph(self) -> rdflib.Graph:
        # Service description returned when no query provided
        service_description_ttl = settings.DICTIONARIES_SERVICE_DESCRIPTION_TTL_FMT.format(
            public_url=self.request.build_absolute_uri(),
            title=settings.DICTIONARIES_DEFAULT_TITLE,
            description=settings.DICTIONARIES_DEFAULT_DESCRIPTION.replace("\n", ""),
        )
        graph = Graph()
        graph.parse(data=service_description_ttl, format="ttl")
        # service_graph.parse('app/service-description.ttl', format="ttl")

        # Add custom functions URI to the service description
        for custom_function_uri in settings.DICTIONARIES_FUNCTIONS:
            graph.add(
                (
                    URIRef(custom_function_uri),
                    RDF.type,
                    URIRef("http://www.w3.org/ns/sparql-service-description#Function"),
                )
            )
            graph.add(
                (
                    URIRef(self.request.build_absolute_uri()),
                    URIRef("http://www.w3.org/ns/sparql-service-description#extensionFunction"),
                    URIRef(custom_function_uri),
                )
            )

        return graph

    def get(self, request: HttpRequest) -> HttpResponse:
        query = request.GET.get("query")
        return self._handle_sparql_request(request, query=query)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Send a SPARQL query to be executed through HTTP POST operation.

        :param request: The HTTP POST request with a .body()
        """
        body = request.body.decode("utf-8")
        content_type = request.headers.get("content-type")
        if content_type == "application/sparql-query":
            query = body
            update = None
        elif content_type == "application/sparql-update":
            query = None
            update = body
        elif content_type == "application/x-www-form-urlencoded":
            request_params = parse.parse_qsl(body)
            query_params = [kvp[1] for kvp in request_params if kvp[0] == "query"]
            query = parse.unquote(query_params[0]) if query_params else None
            update_params = [kvp[1] for kvp in request_params if kvp[0] == "update"]
            update = parse.unquote(update_params[0]) if update_params else None
            # TODO: handle params `using-graph-uri` and `using-named-graph-uri`
            # https://www.w3.org/TR/sparql11-protocol/#update-operation
        else:
            # Response with the service description
            query = None
            update = None

        return self._handle_sparql_request(request, query, update)
