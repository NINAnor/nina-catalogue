from urllib.parse import urlencode

import pytest
from django.test.client import Client
from django.urls import reverse
from rdflib import RDFS, Literal, URIRef
from rdflib_django.utils import get_conjunctive_graph

pytestmark = pytest.mark.django_db(transaction=True)

endpoint = Client()
url = reverse("sparql")


@pytest.fixture(autouse=True)
def set_django_settings(settings):
    settings.DICTIONARIES_ENABLE_UPDATE = True


def test_service_description(settings):
    response = endpoint.get(url, headers={"accept": "text/turtle"})
    public_url = response.wsgi_request.build_absolute_uri()
    # print(response.text.strip())
    assert response.status_code == 200
    assert (
        response.content.decode("utf-8").strip()
        == service_description(public_url, settings.DICTIONARIES_DEFAULT_DESCRIPTION).strip()
    )

    response = endpoint.post(url, headers={"accept": "text/turtle"})
    public_url = response.wsgi_request.build_absolute_uri()
    assert response.status_code == 200
    assert (
        response.content.decode("utf-8").strip()
        == service_description(public_url, settings.DICTIONARIES_DEFAULT_DESCRIPTION).strip()
    )

    # Check for application/xml
    response = endpoint.post(url, headers={"accept": "application/xml"})
    assert response.status_code == 200


def test_custom_concat_json():
    response = endpoint.get(url, data={"query": concat_select}, headers={"accept": "application/json"})
    # print(response.json())
    assert response.status_code == 200
    assert response.json()["results"]["bindings"][0]["concat"]["value"] == "Firstlast"

    response = endpoint.post(
        url,
        data=urlencode({"query": concat_select}),
        headers={"accept": "application/json"},
        content_type="application/x-www-form-urlencoded",
    )
    print(response.content.decode("utf-8"))
    assert response.status_code == 200
    assert response.json()["results"]["bindings"][0]["concat"]["value"] == "Firstlast"

    response = endpoint.post(
        url, data=concat_select, headers={"accept": "application/json"}, content_type="application/sparql-query"
    )
    assert response.status_code == 200
    assert response.json()["results"]["bindings"][0]["concat"]["value"] == "Firstlast"


def test_select_noaccept_xml():
    response = endpoint.post(url, data={"query": concat_select})
    assert response.status_code == 200


def test_select_csv():
    response = endpoint.post(url, data={"query": concat_select}, headers={"accept": "text/csv"})
    assert response.status_code == 200


label_patch = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
DELETE { ?subject rdfs:label "foo" }
INSERT { ?subject rdfs:label "bar" }
WHERE { ?subject rdfs:label "foo" }
"""


@pytest.mark.parametrize(
    "api_key,key_provided,param_method",
    [
        (api_key, key_provided, param_method)
        for api_key in [None, "key"]
        for key_provided in [True, False]
        for param_method in ["body_form", "body_direct"]
    ],
)
def test_sparql_update(api_key, key_provided, param_method, settings):
    settings.DICTIONARIES_RDFLIB_APIKEY = api_key

    graph = get_conjunctive_graph()

    subject = URIRef("http://server.test/subject")
    headers = {}
    if key_provided:
        headers["Authorization"] = "Bearer key"
    graph.add((subject, RDFS.label, Literal("foo")))
    if param_method == "body_form":
        request_args = {
            "data": urlencode({"update": label_patch}),
            "content_type": "application/x-www-form-urlencoded",
        }
    else:
        # direct
        request_args = {"data": label_patch, "content_type": "application/sparql-update"}
    response = endpoint.post(url, headers=headers, **request_args)
    if api_key is None or key_provided:
        assert response.status_code == 204
        assert (subject, RDFS.label, Literal("foo")) not in graph
        assert (subject, RDFS.label, Literal("bar")) in graph
    else:
        assert response.status_code == 403
        assert (subject, RDFS.label, Literal("foo")) in graph
        assert (subject, RDFS.label, Literal("bar")) not in graph


def test_sparql_query_update_fail():
    response = endpoint.post(
        url, data=urlencode({"update": label_patch, "query": label_patch}), content_type="application/sparql-update"
    )
    assert response.status_code == 400


def test_multiple_accept_return_json():
    response = endpoint.get(
        url,
        data={"query": concat_select},
        headers={"accept": "text/html;q=0.3, application/xml;q=0.9, application/json, */*;q=0.8"},
    )
    assert response.status_code == 200
    assert response.json()["results"]["bindings"][0]["concat"]["value"] == "Firstlast"


def test_multiple_accept_return_json2():
    response = endpoint.get(
        url,
        data={"query": concat_select},
        headers={"accept": "text/html;q=0.3, application/json, application/xml;q=0.9, */*;q=0.8"},
    )
    assert response.status_code == 200
    assert response.json()["results"]["bindings"][0]["concat"]["value"] == "Firstlast"


def test_fail_select_turtle():
    response = endpoint.post(
        url,
        data=urlencode({"query": concat_select}),
        headers={"accept": "text/turtle"},
        content_type="application/x-www-form-urlencoded",
    )
    assert response.status_code == 422
    # assert response.json()['results']['bindings'][0]['concat']['value'] == "Firstlast"


def test_concat_construct_turtle():
    # expected to return turtle
    response = endpoint.post(
        url,
        data=urlencode({"query": custom_concat_construct}),
        headers={"accept": "application/json"},
        content_type="application/x-www-form-urlencoded",
    )
    assert response.status_code == 200
    # assert response.json()['results']['bindings'][0]['concat']['value'] == "Firstlast"


def test_concat_construct_xml():
    # expected to return turtle
    response = endpoint.post(
        url,
        data={"query": custom_concat_construct},
        headers={"accept": "application/xml"},
    )
    assert response.status_code == 200


def test_yasgui():
    # expected to return turtle
    response = endpoint.get(
        url,
        headers={"accept": "text/html"},
    )
    assert response.status_code == 200


def test_bad_request():
    response = endpoint.get(f"{url}?query=figarofigarofigaro", headers={"accept": "application/json"})
    assert response.status_code == 400


concat_select = """PREFIX myfunctions: <https://w3id.org/um/sparql-functions/>
SELECT ?concat ?concatLength WHERE {
    BIND("First" AS ?first)
    BIND(myfunctions:custom_concat(?first, "last") AS ?concat)
}"""

custom_concat_construct = """PREFIX myfunctions: <https://w3id.org/um/sparql-functions/>
CONSTRUCT {
    <http://test> <http://concat> ?concat, ?concatLength .
} WHERE {
    BIND("First" AS ?first)
    BIND(myfunctions:custom_concat(?first, "last") AS ?concat)
}"""


def service_description(public_url, description):
    return f"""@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix ent: <http://www.w3.org/ns/entailment/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sd: <http://www.w3.org/ns/sparql-service-description#> .

<{public_url}> a sd:Service ;
    rdfs:label "SPARQL endpoint for RDFLib graph" ;
    dc:description "{description}" ;
    sd:defaultDataset [ a sd:Dataset ;
            sd:defaultGraph [ a sd:Graph ] ] ;
    sd:defaultEntailmentRegime ent:RDFS ;
    sd:endpoint <{public_url}> ;
    sd:extensionFunction <https://w3id.org/um/sparql-functions/custom_concat> ;
    sd:feature sd:DereferencesURIs ;
    sd:resultFormat <http://www.w3.org/ns/formats/SPARQL_Results_CSV>,
        <http://www.w3.org/ns/formats/SPARQL_Results_JSON> ;
    sd:supportedLanguage sd:SPARQL11Query .

<https://w3id.org/um/sparql-functions/custom_concat> a sd:Function .
"""
