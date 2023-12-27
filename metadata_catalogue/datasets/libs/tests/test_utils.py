from django.test.client import RequestFactory

from ..utils import req_to_base, safe_get


class TestClass:
    def __init__(self, value=None) -> None:
        self.test = value


def test_safe_get():
    assert safe_get(None, "test") == ""
    assert safe_get(TestClass(), "test") == ""
    assert safe_get(TestClass(), "test2") == ""
    assert safe_get(TestClass("test"), "test") == "test"


def test_req_to_base():
    factory = RequestFactory()
    assert req_to_base(factory.get("/")) == "http://testserver"
    assert req_to_base(factory.get("/api/", secure=True)) == "https://testserver"
