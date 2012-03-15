# encoding: utf-8
import unittest

from nose.plugins.skip import SkipTest

from uricore import IRI, URI
from uricore.wkz_datastructures import MultiDict


class TestURICore(unittest.TestCase):

    def setUp(self):
        self.uri = URI("http://example.com?foo=bar")

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

    def test_hashability(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        iri2 = IRI(u'http://\N{SNOWMAN}/')
        uri = iri.to_uri()

        self.assertNotEquals(hash(iri), hash(uri))
        self.assertEquals(hash(iri), hash(iri2))

    def test_equality(self):
        iri = IRI(u'http://\N{SNOWMAN}/')
        iri2 = IRI(u'http://\N{SNOWMAN}/')
        iri3 = IRI(u'http://\N{SNOWMAN}/?x=2')
        self.assertEquals(iri, iri2)
        self.assertNotEquals(iri, iri3)

    def test_configurable_multi_dict_class(self):
        class CustomMultiDict(MultiDict):
            pass
        iri = IRI(u'http://\N{SNOWMAN}/', query_cls=CustomMultiDict)
        self.assertTrue(isinstance(iri.query, CustomMultiDict))

    def test_from_lenient(self):
        raise SkipTest("not implemented yet")
        lenient_iri = IRI.from_lenient(u'http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)')
        self.assertEquals(repr(lenient_iri), "URI('http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29')")


class TestInterface(unittest.TestCase):

    def setUp(self):
        raise SkipTest('old tests')
        self.fixture = resources.Resource("http://example.com")

    def test_copy_on_update(self):
        url2 = self.fixture.update(scheme="https")
        self.assertNotEquals(self.fixture, url2)

    def test_idn_ascii_encoding(self):
        ascii_url = "http://xn--bcher-kva.ch/".encode('ascii')
        url = resources.Resource(u"http://Bücher.ch/")
        self.assertEquals(url.to_ascii(), ascii_url)

    def test_idn_ascii_poo_encoding(self):
        ascii_url = "http://xn--ls8h.la/".encode('ascii')
        url = resources.Resource("http://💩.la/")
        self.assertEquals(url.to_ascii(), ascii_url)

    def test_getattr(self):
        self.assertEquals(self.fixture.scheme, 'http')

    def test_setattr(self):
        self.assertRaises(AttributeError, setattr, self.fixture.scheme, "")
