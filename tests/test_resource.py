# encoding: utf-8
import unittest

from resources import URI
from resources import IRI
from wkz_datastructures import MultiDict


class TestResources(unittest.TestCase):

    def setUp(self):
        self.uri = URI("http://example.com?foo=bar")

    def test_iri_add_port(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        new_iri = iri.replace(port=8000)
        assert repr(new_iri) == "IRI('http://xn--n3h:8000/')"
        assert iri.port == 8000
        assert iri.port is None

    def test_iri_update_query(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        iriq = iri.update_query({'foo': u'42'})
        assert repr(iri.query) == "MultiDict()"
        assert repr(iriq) == "IRI('http://xn--n3h/?foo=42')"
        assert repr(iriq.query) == "MultiDict([('foo', '42')])"
        iriq2 = iriq.update_query(foo=None)
        assert repr(iriq2) == "IRI('http://xn--n3h/')"
        assert repr(iriq.query) == "MultiDict([('foo', '42')])"

    def test_query_is_immutable(self):
        self.assertRaises(TypeError, self.uri.query.add, "foo", "baz")
        self.assertEquals(set(['bar']), set(self.uri.query.getlist('foo')))

    def test_hashability(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        uri = URI('http://xn--n3h/')
        assert hash(iri) != hash(uri)

    def test_configurable_multi_dict_class(self):
        class CustomMultiDict(MultiDict):
            pass
        iri = IRI(u'http://\N{SNOWMAN}/', query_class=CustomMultiDict)
        assert isinstance(iri.query, CustomMultiDict)

    def test_join_iri(self):
        iri_d = IRI(u'http://\N{SNOWMAN}/')
        iri_p = IRI(u'/path/to/thing')
        iri_j = iri_d.join(iri_p)
        assert repr(iri_j) == "IRI(u'http://\u2603/path/to/thing')"

    def test_join_uri(self):
        uri_d = URI('http://\N{SNOWMAN}/')
        uri_p = URI('/path/to/thing')
        uri_j = uri_d.join(uri_p)
        assert repr(uri_j) == "URI('http://\u2603/path/to/thing')"

    def test_cant_join_strings(self):
        iri_d = IRI(u'http://\N{SNOWMAN}/')
        self.assertRaises(TypeError, iri_d.join, u'/path/to/thing')
        uri_d = URI(u'http://\N{SNOWMAN}/')
        self.assertRaises(TypeError, uri_d.join, '/path/to/thing')

    def test_from_lenient(self):
        lenient_iri = IRI.from_lenient(u'http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)')
        assert repr(lenient_iri) == "URI('http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29')"
