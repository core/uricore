# encoding: utf-8
from __future__ import unicode_literals
import unittest

from resources import URI
from resources import IRI
from wkz_datastructures import MultiDict


class TestIRISnowman(unittest.TestCase):

    def setUp(self):
        self.iri = IRI("http://u:p@www.\N{SNOWMAN}:80/path")

    def test_repr(self):
        expect = "IRI('http://www.xn--n3h/path', encoding='idna')"
        expect = expect.encode('ascii')
        self.assertEquals(repr(self.iri), expect)

    def test_netloc(self):
        expect = "u:p@www.\u2603:80"
        self.assertEquals(self.iri.netloc, expect)

    def test_hostname(self):
        expect = "www.\u2603"
        self.assertEquals(self.iri.hostname, expect)

    def test_port(self):
        expect = "80"
        self.assertEquals(self.iri.port, expect)

    def test_path(self):
        expect = "/path"
        self.assertEquals(self.iri.path, expect)


class TestURISnowman(unittest.TestCase):

    def setUp(self):
        uri = "http://u:p@" + "www.\N{SNOWMAN}".encode('idna') + ":80/path"
        self.uri = URI(uri)

    def test_repr(self):
        expect = "URI('http://www.xn--n3h/path', encoding='idna')".encode('ascii')
        self.assertEquals(repr(self.uri), expect)

    def test_netloc(self):
        expect = "u:p@www.xn--n3h:80".encode('ascii')
        self.assertEquals(self.uri.netloc, expect)

    def test_hostname(self):
        expect = "www.xn--n3h".encode('ascii')
        self.assertEquals(self.uri.hostname, expect)

    def test_port(self):
        expect = "80"
        self.assertEquals(self.uri.port, expect)

    def test_path(self):
        expect = "/path".encode('ascii')
        self.assertEquals(self.uri.path, expect)


class TestResources(unittest.TestCase):

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
