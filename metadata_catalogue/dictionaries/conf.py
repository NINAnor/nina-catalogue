from appconf import AppConf
from django.conf import settings

from .rdf_functions import custom_concat


class DictionariesConf(AppConf):
    DEFAULT_TITLE: str = "SPARQL endpoint for RDFLib graph"
    DEFAULT_DESCRIPTION: str = (
        "A SPARQL endpoint to serve machine learning models, or any other logic implemented in Python."
    )
    DEFAULT_VERSION: str = "0.1.0"
    DEFAULT_FAVICON: str = "https://rdflib.readthedocs.io/en/stable/_static/RDFlib.png"
    DEFAULT_EXAMPLE = """\
    PREFIX myfunctions: <https://w3id.org/um/sparql-functions/>

    SELECT ?concat ?concatLength WHERE {
        BIND("First" AS ?first)
        BIND(myfunctions:custom_concat(?first, "last") AS ?concat)
    }
    """.rstrip()

    SERVICE_DESCRIPTION_TTL_FMT = """\
    @prefix sd: <http://www.w3.org/ns/sparql-service-description#> .
    @prefix ent: <http://www.w3.org/ns/entailment/> .
    @prefix prof: <http://www.w3.org/ns/owl-profile/> .
    @prefix void: <http://rdfs.org/ns/void#> .
    @prefix dc: <http://purl.org/dc/elements/1.1/> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    <{public_url}> a sd:Service ;
        rdfs:label "{title}" ;
        dc:description "{description}" ;
        sd:endpoint <{public_url}> ;
        sd:supportedLanguage sd:SPARQL11Query ;
        sd:resultFormat <http://www.w3.org/ns/formats/SPARQL_Results_JSON>, <http://www.w3.org/ns/formats/SPARQL_Results_CSV> ;
        sd:feature sd:DereferencesURIs ;
        sd:defaultEntailmentRegime ent:RDFS ;
        sd:defaultDataset [
            a sd:Dataset ;
            sd:defaultGraph [
                a sd:Graph ;
            ]
        ] .
    """.rstrip()

    #: This is default for federated queries
    DEFAULT_CONTENT_TYPE = "application/xml"

    #: A mapping from content types to the keys used for serializing
    #: in :meth:`rdflib.Graph.serialize` and other serialization functions
    CONTENT_TYPE_TO_RDFLIB_FORMAT = {
        # https://www.w3.org/TR/sparql11-results-json/
        "application/sparql-results+json": "json",
        "application/json": "json",
        "text/json": "json",
        # https://www.w3.org/TR/rdf-sparql-XMLres/
        "application/sparql-results+xml": "xml",
        "application/xml": "xml",  # for compatibility
        "application/rdf+xml": "xml",  # for compatibility
        "text/xml": "xml",  # not standard
        # https://www.w3.org/TR/sparql11-results-csv-tsv/
        "application/sparql-results+csv": "csv",
        "text/csv": "csv",  # for compatibility
        # Extras
        "text/turtle": "ttl",
    }

    CUSTOM_EVAL = None
    FUNCTIONS = {
        "https://w3id.org/um/sparql-functions/custom_concat": custom_concat,
    }
    EXAMPLE_QUERIES = None
    ENABLE_UPDATE = False
    PROCESSOR = "sparql"
    RDFLIB_APIKEY = None
