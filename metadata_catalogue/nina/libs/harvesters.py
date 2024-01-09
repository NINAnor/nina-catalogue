from typing import Dict

import requests

from metadata_catalogue.datasets.models import Organization

from ..models import Category, Department, Project


def _fetch_paginated_project(url: str, limit=50):
    offset = 0
    found = None

    while found is None or found == limit:
        query = f"{url}?rows={limit}&start={offset}"
        response = requests.get(query)
        if response.status_code == 200:
            data = response.json()

            results = data.get("result").get("results")
            if results:
                yield results
            else:
                break

            offset += limit
            found = data.get("result").get("count")
        else:
            response.raise_for_status()


def _process_project(project: dict):
    p, created = Project.objects.get_or_create(
        extid=project.get("id"),
        defaults={
            "extid": project.get("id"),
            "name": project.get("title"),
            "description": project.get("notes"),
        },
    )
    if created:
        slug = f'prj-{project.get("id")}'
        p.slug = slug

    p.status = project.get("project_state")
    p.budget = project.get("budget")
    p.start_date = project.get("startdate")
    p.end_date = project.get("enddate")

    p.category, _ = Category.objects.get_or_create(name=project.get("category"))
    p.customer, _ = Organization.objects.get_or_create(name=project.get("customer"))

    for group in project.get("groups"):
        slug = f'dpt-{project.get("id")}'
        d, created = Department.objects.get_or_create(
            extid=group.get("id"),
            defaults={
                "name": group.get("title"),
                "description": group.get("description"),
            },
        )
        if created:
            d.slug = slug
            d.save()

        p.departments.add(d)

    p.save()


def prosjektoversikt(url: str, limit=50):
    """
    Harvest projects and departments from prosjekt oversikt APIs
    NOTE: API scheme resembles the CKAN APIs

    Attributes:
        url (str): URL of the Prosjekt Oversikt API, it should point to the base url (just before the `/api/`) without trailing /
            example: https://prosjekt-oversikt.nina.no/ckan
    """

    for projects in _fetch_paginated_project(f"{url}/api/3/action/package_search", limit=limit):
        for project in projects:
            _process_project(project)
