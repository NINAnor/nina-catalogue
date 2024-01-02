import pytest
from django.core.files.base import ContentFile
from django.test.client import RequestFactory
from slugify import slugify

from ..models import Layer, Map, RasterSource, Source, VectorSource
from ..schema import MapStyle

pytestmark = pytest.mark.django_db(transaction=True)


class TestSource:
    def setup_method(self):
        self.source_class = Source
        self.type = None
        self.name = lambda instance: str(instance.name)
        self.factory = RequestFactory()

    def test_slug(self):
        s = self.source_class.objects.create(name="test")

        assert s.slug == slugify("test")
        s.name = "test2"
        s.save()
        assert s.slug == slugify("test")

        s.slug = "test2"
        s.save()
        assert s.slug == slugify("test2")

    def test_name(self):
        s = self.source_class.objects.create(name="test")

        assert str(s) == self.name(s)

    def test_property_type(self):
        s = self.source_class.objects.create(name="test")

        assert s.type == self.type


class TestRasterSource(TestSource):
    def setup_method(self):
        super().setup_method()
        self.source_class = RasterSource
        self.type = "raster"

    def test_download_url(self):
        s = self.source_class.objects.create(name="test", url="http://test.com")

        request = self.factory.get("/")

        assert s.get_download_url(request) == s.url

        s.original_data = ContentFile(b"", name="foo.png")
        s.save()
        assert s.original_data.url in s.get_download_url(request)

    def test_source_url(self):
        s = self.source_class.objects.create(name="test", url="http://test.com")

        request = self.factory.get("/")

        assert s.get_source_url(request) == s.url

        s.source = ContentFile(b"", name="foo.png")
        s.save()
        assert s.source.url in s.get_source_url(request)


class TestVectorSource(TestRasterSource):
    def setup_method(self):
        super().setup_method()
        self.source_class = VectorSource
        self.type = "vector"


class TestLayer:
    def test_save(self):
        s = VectorSource.objects.create(name="test", url="http://test.com", default_layer="data")
        m = Map.objects.create(
            title="Test",
        )
        l = Layer.objects.create(source=s, map=m)

        assert l.name == s.name
        assert l.slug == s.slug
        assert l.source_layer == s.default_layer
        l.delete()

        l = Layer.objects.create(source=s, map=m, source_layer="test")

        assert l.source_layer == "test"
        l.delete()

        l = Layer.objects.create(map=m)

        assert l.slug == "baselayer"
        assert l.name == "Unnamed"
        l.delete()

        s = RasterSource.objects.create(
            name="test-raster",
            url="http://test.com",
        )
        l = Layer.objects.create(source=s, map=m)
        assert l.source_layer == None


class TestMap:
    def test_slug(self):
        m = Map.objects.create(title="test")

        assert m.slug == slugify("test")
        m.title = "test2"
        m.save()
        assert m.slug == slugify("test")

        m.slug = "test2"
        m.save()
        assert m.slug == slugify("test2")

    def test_metadata(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

        m = Map.objects.create(title="test", subtitle="subtitle")

        metadata = m.get_metadata(self.request)

        assert "style" in metadata
        assert "subtitle" in metadata and metadata["subtitle"] == "subtitle"
        assert metadata["layers"] == []

    def test_style(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

        m = Map.objects.create(title="test", subtitle="subtitle")

        s1 = VectorSource.objects.create(
            name="test",
            source=ContentFile(b"", name="foo.pmtiles"),
            protocol="pmtiles",
        )
        s2 = VectorSource.objects.create(name="test2", url="http://test.com", default_layer="data")

        Layer.objects.create(
            source=s1,
            map=m,
        )

        Layer.objects.create(
            source=s2,
            map=m,
        )

        style = m.get_style(self.request)

        assert MapStyle.model_validate(style)
