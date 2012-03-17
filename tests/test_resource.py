# encoding: utf-8
import unittest

from nose.plugins.skip import SkipTest

from uricore import IRI, URI
from uricore.wkz_datastructures import MultiDict


class TestURICore(unittest.TestCase):

    def setUp(self):
        self.uri = URI("http://example.com?foo=bar")

    def test_hashability(self):
        iri1 = IRI(u'http://\N{CLOUD}/')
        iri2 = IRI(u'http://\N{CLOUD}/')
        self.assertEquals(hash(iri1), hash(iri2))

        uri1 = URI(iri1)
        uri2 = URI('http://xn--l3h/')
        self.assertEquals(hash(uri1), hash(uri2))

        self.assertNotEquals(hash(iri1), hash(uri1))

    def test_equality(self):
        iri1 = IRI(u'http://\N{CLOUD}/')
        iri2 = IRI(u'http://\N{CLOUD}/')
        self.assertEquals(iri1, iri2)

        uri1 = URI(iri1)
        uri2 = URI('http://xn--l3h/')
        self.assertEquals(uri1, uri2)

        self.assertNotEquals(iri1, uri1)

    def test_query_param_breaks_equality_(self):
        iri = IRI(u'http://\N{CLOUD}/')
        iri2 = IRI(u'http://\N{CLOUD}/?q=a')
        self.assertNotEquals(iri, iri2)

    def test_iri_add_port(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        new_iri = iri.update(port=8000)
        self.assertEquals(iri.netloc + ':8000', new_iri.netloc)
        self.assertEquals(new_iri.port, '8000')
        self.assertEquals(iri.port, None)

    def test_iri_update_query(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        q = iri.query
        q.update({'foo': u'42'})
        iri2 = iri.update_query(q)
        self.assertNotEquals(iri, iri2)
        self.assertTrue(isinstance(iri2, IRI))
        self.assertEquals(repr(iri.query), "MultiDict([])")
        self.assertEquals(repr(iri2), "IRI(u'http://\u2603/?foo=42')")
        self.assertEquals(repr(iri2.query), "MultiDict([('foo', u'42')])")

    def test_query_is_immutable(self):
        self.uri.query.add("foo", "baz")
        self.assertEquals(set(['bar']), set(self.uri.query.getlist('foo')))

    def test_configurable_multi_dict_class(self):
        class CustomMultiDict(MultiDict):
            pass
        iri = IRI(u'http://\N{SNOWMAN}/', query_cls=CustomMultiDict)
        self.assertTrue(isinstance(iri.query, CustomMultiDict))

    def test_from_lenient(self):
        raise SkipTest("Not Implemented")
        lenient_iri = IRI.from_lenient(u'http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)')
        self.assertEquals(repr(lenient_iri), "URI('http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29')")

    def test_normalizes_identifier(self):
        uri = URI('http://example.com/#')
        self.assertEquals(str(uri), 'http://example.com/')
