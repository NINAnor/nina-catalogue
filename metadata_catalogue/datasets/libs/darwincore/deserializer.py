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


def text_or_null(node, strip=False):
    if not node:
        return None

    if strip:
        return node.text.strip()

    return node.text


def to_date(node):
    if not node:
        return None

    return datetime.strptime(node.text.strip(), "%Y-%m-%d")


def person_from_block(block):
    data = {
        "first_name": None,
        "last_name": None,
        "email": None,
        "position": None,
        "belongs_to_id": None,
        "country_id": None,
    }

    if individual := block.find("individualName"):
        data["first_name"] = text_or_null(individual.find("givenName"))
        data["last_name"] = text_or_null(individual.find("surName"))

    data["email"] = text_or_null(block.find("electronicMailAddress"))

    data["position"] = text_or_null(block.find("positionName"))

    if address := block.find("address"):
        if country := address.find("country"):
            data["country_id"] = Country.objects.filter(iso=country.text).first().pk

    if org := block.find("organizationName"):
        o, _ = Organization.objects.get_or_create(name=org.text)
        data["belongs_to_id"] = o.id

    p, _ = Person.objects.get_or_create(**data)

    for identifier in block.find_all("userId"):
        PersonIdentifier.objects.get_or_create(person=p, type=identifier["directory"], value=identifier.text)

    return p


def to_metadata(xml_path: pathlib.Path, dataset: Dataset):
    with open(str(xml_path)) as eml:
        soup = BeautifulSoup(eml, features="lxml-xml")
        with transaction.atomic():
            metadata = dataset.get_metadata()

            dataset = soup.find("dataset")
            metadata.title = text_or_null(dataset.find("title"))
            metadata.abstract = text_or_null(dataset.find("abstract"), strip=True)

            for identifier in dataset.find_all("alternateIdentifier"):
                source = (
                    MetadataIdentifier.Type.IPT if "ipt.nina.no" in identifier.text else MetadataIdentifier.Type.GBIF
                )
                MetadataIdentifier.objects.get_or_create(
                    metadata=metadata, identifier=identifier.text, defaults={"source": source}
                )

            for person in dataset.find_all("creator"):
                pr, _ = PersonRole.objects.get_or_create(
                    person=person_from_block(person),
                    metadata=metadata,
                    role=PersonRole.RoleType.CREATOR,
                )
                metadata.people.add(pr)

            for person in dataset.find_all("metadataProvider"):
                pr, _ = PersonRole.objects.get_or_create(
                    person=person_from_block(person),
                    metadata=metadata,
                    role=PersonRole.RoleType.PROVIDER,
                )
                metadata.people.add(pr)

            for person in dataset.find_all("associatedParty"):
                pr, _ = PersonRole.objects.get_or_create(
                    person=person_from_block(person),
                    metadata=metadata,
                    role=PersonRole.RoleType.ASSOCIATED_PARTY,
                )
                metadata.people.add(pr)

            metadata.date_publication = to_date(dataset.find("pubDate"))
            if language := dataset.find("language"):
                metadata.language = Language.objects.filter(iso_639_2T=language.text).first()

            if intellectual_rights := dataset.find("intellectualRights"):
                name = text_or_null(intellectual_rights.find("citetitle"))
                url = intellectual_rights.find("ulink")["url"] if intellectual_rights.find("ulink") else None
                license, _ = License.objects.get_or_create(name=name, url=url)
                metadata.license = license

            if maintenance := dataset.find("maintenance"):
                metadata.maintenance_update_description = text_or_null(maintenance.find("description"))

            metadata.maintenance_update_description = text_or_null(dataset.find("maintenanceUpdateFrequency"))

            metadata.geographic_description = text_or_null(dataset.find("geographicDescription"))
            # bounding box
            if coords := dataset.find("boundingCoordinates"):
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

            if taxonomy_coverage := dataset.find("taxonomicCoverage"):
                for classification in taxonomy_coverage.find_all("taxonomicClassification"):
                    taxonomy_type = None
                    if rank := classification.find("taxonRankName"):
                        taxonomy_type, _ = TaxonomyType.objects.get_or_create(name=rank.text)

                    taxonomy, _ = Taxonomy.objects.get_or_create(
                        defaults={"common": text_or_null(classification.find("commonName"))},
                        name=classification.find("taxonRankValue").text,
                        type=taxonomy_type,
                    )
                    metadata.taxonomies.add(taxonomy)

            for contact in dataset.find_all("contact"):
                pr, _ = PersonRole.objects.get_or_create(
                    person=person_from_block(contact), metadata=metadata, role=PersonRole.RoleType.CONTACT
                )
                metadata.people.add(pr)

            project = dataset.find("project")
            if project:
                metadata.project_id = project["id"] if "id" in project else None
                metadata.project_title = project.find("title").text if project.find("title") else None
                metadata.project_abstract = project.find("abstract").text.strip() if project.find("abstract") else None

                if funding := project.find("funding"):
                    for org in funding.find_all("para"):
                        o, _ = Organization.objects.get_or_create(name=org.text)
                        org_role, _ = OrganizationRole.objects.get_or_create(
                            organization=o,
                            metadata=metadata,
                            role=OrganizationRole.RoleType.FUNDING,
                        )
                        metadata.organizations.add(org_role)

                for personnel in project.find_all("personnel"):
                    pr, _ = PersonRole.objects.get_or_create(
                        person=person_from_block(personnel),
                        metadata=metadata,
                        role=PersonRole.RoleType.PROJECT_PERSONNEL,
                    )
                    metadata.people.add(pr)

                if project.find("studyAreaDescription") and project.find("studyAreaDescription").find("descriptor"):
                    metadata.project_study_area_description = (
                        project.find("studyAreaDescription").find("descriptor").text.strip()
                    )
                if project.find("designDescription") and project.find("designDescription").find("description"):
                    metadata.project_design_description = (
                        project.find("designDescription").find("description").text.strip()
                    )

            gbif = soup.find("additionalMetadata").find("gbif")
            if cit := gbif.find("citation"):
                c, _ = Citation.objects.get_or_create(text=cit.text)
                metadata.citation = c

            if bibliography := gbif.find("bibliography"):
                for citation in bibliography.find_all("citation"):
                    c, _ = Citation.objects.get_or_create(
                        text=citation.text, identifier=citation["identifier"] if "identifier" in citation else None
                    )
                    metadata.bibliography.add(c)

            metadata.logo_url = gbif.find("resourceLogoUrl").text if gbif.find("resourceLogoUrl") else None

            if formation_period := gbif.find("formationPeriod"):
                try:
                    periods = [int(year) for year in (formation_period.text).split("-")]
                    if len(periods) == 2:
                        metadata.formation_period_start = datetime(periods[0], 1, 1)
                        metadata.formation_period_end = datetime(periods[1], 1, 1)
                    elif len(periods) == 1:
                        metadata.formation_period_start = datetime(periods[0], 1, 1)
                        metadata.formation_period_end = datetime(periods[0], 1, 1)
                except ValueError:
                    metadata.formation_period_description = formation_period.text

            for keyword_set in dataset.find_all("keywordSet"):
                thesaurus = text_or_null(keyword_set.find("keywordThesaurus"))
                match = re.search(r"(?P<url>https?://[^\s]+)", thesaurus)
                definition = match.group("url") if match else None

                for kw in keyword_set.find_all("keyword"):
                    k, _ = Keyword.objects.get_or_create(
                        name=text_or_null(kw), definition=definition, description=thesaurus
                    )
                    metadata.keywords.add(k)

            metadata.save()
