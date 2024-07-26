# =================================================================
#
# Authors: Francesco Bartoli <francesco.bartoli@geobeyond.it>
#          Luca Delucchi <lucadeluge@gmail.com>
#          Krishna Lodha <krishnaglodha@gmail.com>
#          Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2022 Francesco Bartoli
# Copyright (c) 2022 Luca Delucchi
# Copyright (c) 2022 Krishna Lodha
# Copyright (c) 2022 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

"""Integration module for Django"""

from collections.abc import Mapping

from django.http import HttpRequest, HttpResponse
from django.views.decorators.common import no_append_slash
from pygeoapi.api import API

from ..libs.utils import req_to_base
from .models import GeoAPIConfig


@no_append_slash
def landing_page(request: HttpRequest) -> HttpResponse:
    """
    OGC API landing page endpoint

    :request Django HTTP Request

    :returns: Django HTTP Response
    """

    return _feed_response(request, "landing_page")


@no_append_slash
def openapi(request: HttpRequest) -> HttpResponse:
    """
    OpenAPI endpoint

    :request Django HTTP Request

    :returns: Django HTTP Response
    """

    return _feed_response(request, "openapi_")


@no_append_slash
def conformance(request: HttpRequest) -> HttpResponse:
    """
    OGC API conformance endpoint

    :request Django HTTP Request

    :returns: Django HTTP Response
    """

    return _feed_response(request, "conformance")


@no_append_slash
def collections(request: HttpRequest, collection_id: str | None = None) -> HttpResponse:
    """
    OGC API collections endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier

    :returns: Django HTTP Response
    """

    return _feed_response(request, "describe_collections", collection_id)


@no_append_slash
def collection_queryables(request: HttpRequest, collection_id: str | None = None) -> HttpResponse:
    """
    OGC API collections queryables endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier

    :returns: Django HTTP Response
    """

    return _feed_response(request, "get_collection_queryables", collection_id)


@no_append_slash
def collection_items(request: HttpRequest, collection_id: str) -> HttpResponse:
    """
    OGC API collections items endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier

    :returns: Django HTTP response
    """

    if request.method == "GET":
        return _feed_response(
            request,
            "get_collection_items",
            collection_id,
        )
    elif request.method == "POST":
        if request.content_type is not None:
            if request.content_type == "application/geo+json":
                return _feed_response(request, "manage_collection_item", request, "create", collection_id)
            else:
                return _feed_response(request, "post_collection_items", request, collection_id)
    elif request.method == "OPTIONS":
        return _feed_response(request, "manage_collection_item", request, "options", collection_id)


@no_append_slash
def collection_map(request: HttpRequest, collection_id: str):
    """
    OGC API - Maps map render endpoint

    :param collection_id: collection identifier

    :returns: HTTP response
    """

    return _feed_response(request, "get_collection_map", collection_id)


@no_append_slash
def collection_style_map(request: HttpRequest, collection_id: str, style_id: str = None):
    """
    OGC API - Maps map render endpoint

    :param collection_id: collection identifier
    :param collection_id: style identifier

    :returns: HTTP response
    """

    return _feed_response(request, "get_collection_map", collection_id, style_id)


@no_append_slash
def collection_item(request: HttpRequest, collection_id: str, item_id: str) -> HttpResponse:
    """
    OGC API collections items endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier
    :param item_id: item identifier

    :returns: Django HTTP response
    """

    if request.method == "GET":
        return _feed_response(request, "get_collection_item", collection_id, item_id)
    elif request.method == "PUT":
        return _feed_response(request, "manage_collection_item", request, "update", collection_id, item_id)
    elif request.method == "DELETE":
        return _feed_response(request, "manage_collection_item", request, "delete", collection_id, item_id)
    elif request.method == "OPTIONS":
        return _feed_response(
            request,
            "manage_collection_item",
            request,
            "options",
            collection_id,
            item_id,
        )


@no_append_slash
def collection_coverage(request: HttpRequest, collection_id: str) -> HttpResponse:
    """
    OGC API - Coverages coverage endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_collection_coverage", collection_id)


@no_append_slash
def collection_coverage_domainset(request: HttpRequest, collection_id: str) -> HttpResponse:
    """
    OGC API - Coverages coverage domainset endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_collection_coverage_domainset", collection_id)


@no_append_slash
def collection_coverage_rangetype(request: HttpRequest, collection_id: str) -> HttpResponse:
    """
    OGC API - Coverages coverage rangetype endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_collection_coverage_rangetype", collection_id)


@no_append_slash
def collection_tiles(request: HttpRequest, collection_id: str) -> HttpResponse:
    """
    OGC API - Tiles collection tiles endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_collection_tiles", collection_id)


@no_append_slash
def collection_tiles_metadata(request: HttpRequest, collection_id: str, tileMatrixSetId: str) -> HttpResponse:
    """
    OGC API - Tiles collection tiles metadata endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier
    :param tileMatrixSetId: identifier of tile matrix set

    :returns: Django HTTP response
    """

    return _feed_response(
        request,
        "get_collection_tiles_metadata",
        collection_id,
        tileMatrixSetId,
    )


@no_append_slash
def collection_item_tiles(
    request: HttpRequest,
    collection_id: str,
    tileMatrixSetId: str,
    tileMatrix: str,
    tileRow: str,
    tileCol: str,
) -> HttpResponse:
    """
    OGC API - Tiles collection tiles data endpoint

    :request Django HTTP Request
    :param collection_id: collection identifier
    :param tileMatrixSetId: identifier of tile matrix set
    :param tileMatrix: identifier of {z} matrix index
    :param tileRow: identifier of {y} matrix index
    :param tileCol: identifier of {x} matrix index

    :returns: Django HTTP response
    """

    return _feed_response(
        request,
        "get_collection_tiles_metadata",
        collection_id,
        tileMatrixSetId,
        tileMatrix,
        tileRow,
        tileCol,
    )


@no_append_slash
def processes(request: HttpRequest, process_id: str | None = None) -> HttpResponse:
    """
    OGC API - Processes description endpoint

    :request Django HTTP Request
    :param process_id: process identifier

    :returns: Django HTTP response
    """

    return _feed_response(request, "describe_processes", process_id)


@no_append_slash
def jobs(request: HttpRequest, job_id: str | None = None) -> HttpResponse:
    """
    OGC API - Jobs endpoint

    :request Django HTTP Request
    :param process_id: process identifier
    :param job_id: job identifier

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_jobs", job_id)


@no_append_slash
def job_results(request: HttpRequest, job_id: str | None = None) -> HttpResponse:
    """
    OGC API - Job result endpoint

    :request Django HTTP Request
    :param job_id: job identifier

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_job_result", job_id)


@no_append_slash
def job_results_resource(request: HttpRequest, process_id: str, job_id: str, resource: str) -> HttpResponse:
    """
    OGC API - Job result resource endpoint

    :request Django HTTP Request
    :param job_id: job identifier
    :param resource: job resource

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_job_result_resource", job_id, resource)


@no_append_slash
def get_collection_edr_query(request: HttpRequest, collection_id: str, instance_id: str) -> HttpResponse:
    """
    OGC API - EDR endpoint

    :request Django HTTP Request
    :param job_id: job identifier
    :param resource: job resource

    :returns: Django HTTP response
    """

    query_type = request.path.split("/")[-1]
    return _feed_response(request, "get_collection_edr_query", collection_id, instance_id, query_type)


@no_append_slash
def stac_catalog_root(request: HttpRequest) -> HttpResponse:
    """
    STAC root endpoint

    :request Django HTTP Request

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_stac_root")


@no_append_slash
def stac_catalog_path(request: HttpRequest, path: str) -> HttpResponse:
    """
    STAC path endpoint

    :request Django HTTP Request
    :param path: path

    :returns: Django HTTP response
    """

    return _feed_response(request, "get_stac_path", path)


def stac_catalog_search(request: HttpRequest) -> HttpResponse:
    pass


def _to_django_response(headers: Mapping, status_code: int, content: str) -> HttpResponse:
    """Convert API payload to a django response"""

    response = HttpResponse(content, status=status_code)

    for key, value in headers.items():
        response[key] = value
    return response


def _feed_response(request: HttpRequest, api_definition: str, *args, **kwargs) -> HttpResponse:
    """Use pygeoapi api to process the input request"""

    config = GeoAPIConfig.get_solo()
    geoapi_conf, openapi_def = config.get_config(req_to_base(request))
    api_ = API(geoapi_conf, openapi_def)
    api = getattr(api_, api_definition)
    response = api(request, *args, **kwargs)
    return _to_django_response(*response)
