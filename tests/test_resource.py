# encoding: utf-8
import unittest

from nose.plugins.skip import SkipTest

from resources import URI
from resources import IRI
from wkz_datastructures import MultiDict


class TestResources(unittest.TestCase):

    def setUp(self):
        self.uri = URI("http://example.com?foo=bar")

    def test_iri_add_port(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        new_iri = iri.update(port=8000)
        self.assertEquals(iri.netloc + ':8000', new_iri.netloc)
        self.assertEquals(new_iri.port, '8000')
        self.assertEquals(iri.port, None)

    def test_iri_update_query(self):
        raise SkipTest('not implemented')
        iri = IRI(u'http://\N{SNOWMAN}/')
        iriq = iri.update_query({'foo': u'42'})
        self.assertEquals(repr(iri.query), "MultiDict()")
        self.assertEquals(repr(iriq), "IRI('http://xn--n3h/?foo=42')")
        self.assertEquals(repr(iriq.query), "MultiDict([('foo', '42')])")
        iriq2 = iriq.update_query(foo=None)
        self.assertEquals(repr(iriq2), "IRI('http://xn--n3h/')")
        self.assertEquals(repr(iriq.query), "MultiDict([('foo', '42')])")

    def test_query_is_immutable(self):
        self.uri.query.add("foo", "baz")
        self.assertEquals(set(['bar']), set(self.uri.query.getlist('foo')))

    def test_hashability(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        iri2 = IRI(u'http://\N{SNOWMAN}/')
        uri = iri.to_uri()

        self.assertNotEquals(hash(iri), hash(uri))
        self.assertEquals(hash(iri), hash(iri2))

    def test_configurable_multi_dict_class(self):
        class CustomMultiDict(MultiDict):
            pass
        iri = IRI(u'http://\N{SNOWMAN}/', query_cls=CustomMultiDict)
        self.assertTrue(isinstance(iri.query, CustomMultiDict))

    def test_from_lenient(self):
        raise SkipTest("not implemented yet")
        lenient_iri = IRI.from_lenient(u'http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)')
        self.assertEquals(repr(lenient_iri), "URI('http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29')")
