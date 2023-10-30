import pathlib
import re
from datetime import datetime

from bs4 import BeautifulSoup
from countries_plus.models import Country
from django.contrib.gis.geos import Polygon
from django.db import transaction
from languages_plus.models import Language

from metadata_catalogue.datasets.models import (
    Citation,
    Dataset,
    Keyword,
    License,
    MetadataIdentifier,
    Organization,
    OrganizationRole,
    Person,
    PersonIdentifier,
    PersonRole,
    Taxonomy,
    TaxonomyType,
)


def person_from_block(block):
    data = {}

    if individual := block.find("individualName"):
        data["first_name"] = individual.find("givenName").text
        data["last_name"] = individual.find("surName").text

    data["email"] = block.find("electronicMailAddress").text
    data["position"] = block.find("positionName").text if block.find("positionName") else ""

    if address := block.find("address"):
        data["country"] = Country.objects.filter(iso=address.find("country").text).first()

    if org := block.find("organizationName"):
        o, _ = Organization.objects.get_or_create(name=org.text)
        data["belongs_to"] = o

    p, _ = Person.objects.get_or_create(**data)

    for identifier in block.find_all("userId"):
        PersonIdentifier.objects.get_or_create(person=p, type=identifier["directory"], value=identifier.text)

    return p


def to_metadata(xml_path: pathlib.Path, dataset: Dataset):
    with open(str(xml_path)) as eml:
        soup = BeautifulSoup(eml, features="lxml-xml")
        with transaction.atomic():
            metadata = dataset.metadata

            dataset = soup.find("dataset")
            metadata.title = dataset.find("title").text
            metadata.abstract = dataset.find("abstract").text.strip()

            for identifier in dataset.find_all("alternateIdentifier"):
                MetadataIdentifier.objects.get_or_create(metadata=metadata, id=identifier.text)

            metadata.people.add(
                PersonRole.objects.create(
                    person=person_from_block(dataset.find("creator")),
                    metadata=metadata,
                    role=PersonRole.RoleType.CREATOR,
                )
            )
            metadata.people.add(
                PersonRole.objects.create(
                    person=person_from_block(dataset.find("metadataProvider")),
                    metadata=metadata,
                    role=PersonRole.RoleType.PROVIDER,
                )
            )

            metadata.date_publication = datetime.strptime(dataset.find("pubDate").text.strip(), "%Y-%m-%d")
            metadata.language = Language.objects.filter(iso_639_2T=dataset.find("language").text).first()

            license, _ = License.objects.get_or_create(name=dataset.find("intellectualRights").find("citetitle").text)
            metadata.license = license
            metadata.maintenance_update_description = dataset.find("maintenance").find("description").text
            metadata.maintenance_update_description = dataset.find("maintenanceUpdateFrequency").text

            metadata.geographic_description = dataset.find("geographicDescription").text
            # bounding box
            coords = dataset.find("boundingCoordinates")
            poly = Polygon.from_bbox(
                (
                    float(coords.find("westBoundingCoordinate").text),
                    float(coords.find("southBoundingCoordinate").text),
                    float(coords.find("eastBoundingCoordinate").text),
                    float(coords.find("northBoundingCoordinate").text),
                )
            )
            poly.srid = 4326
            metadata.bounding_box = poly

            taxonomy_coverage = dataset.find("taxonomicCoverage")

            for classification in taxonomy_coverage.find_all("taxonomicClassification"):
                taxonomy_type, _ = TaxonomyType.objects.get_or_create(name=classification.find("taxonRankName").text)
                taxonomy, _ = Taxonomy.objects.get_or_create(
                    name=classification.find("taxonRankValue").text, type=taxonomy_type
                )
                metadata.taxonomies.add(taxonomy)

            for contact in dataset.find_all("contact"):
                metadata.people.add(
                    PersonRole.objects.create(
                        person=person_from_block(contact), metadata=metadata, role=PersonRole.RoleType.CONTACT
                    )
                )

            project = dataset.find("project")
            metadata.project_id = project["id"]
            metadata.project_title = project.find("title").text
            metadata.project_abstract = project.find("abstract").text.strip()

            if funding := project.find("funding"):
                for org in funding.find_all("para"):
                    o, _ = Organization.objects.get_or_create(name=org.text)
                    metadata.organizations.add(
                        OrganizationRole.objects.create(
                            organization=o,
                            metadata=metadata,
                            role=OrganizationRole.RoleType.FUNDING,
                        )
                    )

            metadata.project_study_area_description = (
                project.find("studyAreaDescription").find("descriptor").text.strip()
            )
            metadata.project_design_description = project.find("designDescription").find("description").text.strip()

            gbif = soup.find("additionalMetadata").find("gbif")
            c, _ = Citation.objects.get_or_create(text=gbif.find("citation").text)
            metadata.citation = c

            if bibliography := gbif.find("bibliography"):
                for citation in bibliography.find_all("citation"):
                    c, _ = Citation.objects.get_or_create(text=citation.text, identifier=citation["identifier"])
                    metadata.bibliography.add(c)

            metadata.logo_url = gbif.find("resourceLogoUrl").text

            periods = [int(year) for year in (gbif.find("formationPeriod").text).split("-")]

            metadata.formation_period_start = datetime(periods[0], 1, 1)
            metadata.formation_period_end = datetime(periods[1], 1, 1)

            for keyword in dataset.find_all("keywordSet"):
                thesaurus = keyword.find("keywordThesaurus").text
                definition = re.search(r"(?P<url>https?://[^\s]+)", thesaurus).group("url")

                k, _ = Keyword.objects.get_or_create(
                    name=keyword.find("keyword").text, definition=definition, description=thesaurus
                )
                metadata.keywords.add(k)

            metadata.save()
