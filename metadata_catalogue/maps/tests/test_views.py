import uuid
from unittest.mock import patch

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test.client import Client
from django.urls import reverse

from ..enums import Visibility
from ..models import Layer, Map, Portal, PortalMap, VectorSource

pytestmark = pytest.mark.django_db(transaction=True)

TEST_UUIDS = [f"uuid_{i}" for i in range(10000)]


class TestAPI:
    def setup_method(self):
        self.factory = Client()

        User = get_user_model()
        u = User.objects.create(email="test@email.com")
        self.user = u
        self.staff = User.objects.create(email="staff@email.com", is_staff=True)

        m1 = Map.objects.create(title="Public", subtitle="subtitle", visibility=Visibility.PUBLIC)
        m2 = Map.objects.create(title="Private", subtitle="subtitle", visibility=Visibility.PRIVATE, owner=u)

        s1 = VectorSource.objects.create(
            name="test",
            source=ContentFile(b"", name="foo.pmtiles"),
            protocol="pmtiles",
        )
        s2 = VectorSource.objects.create(name="test2", url="http://test.com", default_layer="data")

        Layer.objects.create(
            source=s1,
            map=m1,
        )

        Layer.objects.create(
            source=s2,
            map=m1,
        )

        Layer.objects.create(
            source=s1,
            map=m2,
        )

        Layer.objects.create(
            source=s2,
            map=m2,
        )

        self.p1 = Portal.objects.create(title="test", visibility=Visibility.PUBLIC)
        self.p2 = Portal.objects.create(
            title="test",
            visibility=Visibility.PRIVATE,
            owner=u,
        )

        PortalMap.objects.create(
            map=m1,
            portal=self.p1,
        )

        PortalMap.objects.create(
            map=m2,
            portal=self.p1,
        )

        PortalMap.objects.create(
            map=m1,
            portal=self.p2,
        )

        PortalMap.objects.create(
            map=m2,
            portal=self.p2,
        )

    def test_metadata(self):
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_metadata", kwargs={"map_slug": "public"}))
        assert r.status_code == 200

        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_metadata", kwargs={"map_slug": "private"}))
        assert r.status_code == 404

        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_metadata", kwargs={"map_slug": "null"}))
        assert r.status_code == 404

        self.factory.force_login(self.user)
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_metadata", kwargs={"map_slug": "private"}))
        assert r.status_code == 200
        self.factory.logout()

        self.factory.force_login(self.staff)
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_metadata", kwargs={"map_slug": "private"}))
        assert r.status_code == 200
        self.factory.logout()

    def test_style(self):
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_style", kwargs={"map_slug": "public"}))
        assert r.status_code == 200

        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_style", kwargs={"map_slug": "private"}))
        assert r.status_code == 404

        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_style", kwargs={"map_slug": "null"}))
        assert r.status_code == 404

        self.factory.force_login(self.user)
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_style", kwargs={"map_slug": "private"}))
        assert r.status_code == 200

        self.factory.force_login(self.staff)
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:map_style", kwargs={"map_slug": "private"}))
        assert r.status_code == 200

    def test_portal(self):
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:portals_get", kwargs={"portal_uuid": self.p1.uuid}))
        assert r.status_code == 200

        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:portals_get", kwargs={"portal_uuid": self.p2.uuid}))
        assert r.status_code == 404

        r = self.factory.get(
            reverse(
                f"{settings.MAPS_API_PREFIX}:portals_get",
                kwargs={"portal_uuid": "00000000-0000-0000-0000-000000000000"},
            )
        )
        assert r.status_code == 404

        self.factory.force_login(self.user)
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:portals_get", kwargs={"portal_uuid": self.p2.uuid}))
        assert r.status_code == 200

        self.factory.force_login(self.staff)
        r = self.factory.get(reverse(f"{settings.MAPS_API_PREFIX}:portals_get", kwargs={"portal_uuid": self.p2.uuid}))
        assert r.status_code == 200

    def test_portal_maps(self):
        r = self.factory.get(
            reverse(f"{settings.MAPS_API_PREFIX}:portals_get_maps", kwargs={"portal_uuid": self.p1.uuid})
        )
        assert r.status_code == 200
        assert len(r.json()) == 1

        r = self.factory.get(
            reverse(f"{settings.MAPS_API_PREFIX}:portals_get_maps", kwargs={"portal_uuid": self.p2.uuid})
        )
        assert r.status_code == 404

        r = self.factory.get(
            reverse(
                f"{settings.MAPS_API_PREFIX}:portals_get_maps",
                kwargs={"portal_uuid": "00000000-0000-0000-0000-000000000000"},
            )
        )
        assert r.status_code == 404

        self.factory.force_login(self.user)
        r = self.factory.get(
            reverse(f"{settings.MAPS_API_PREFIX}:portals_get_maps", kwargs={"portal_uuid": self.p1.uuid})
        )
        assert r.status_code == 200
        assert len(r.json()) == 2

        self.factory.force_login(self.staff)
        r = self.factory.get(
            reverse(f"{settings.MAPS_API_PREFIX}:portals_get_maps", kwargs={"portal_uuid": self.p1.uuid})
        )
        assert r.status_code == 200
        assert len(r.json()) == 2
