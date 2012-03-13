# encoding: utf-8
import unittest

from resources import IRI, URI


class TestURISnowman(unittest.TestCase):

    uri = URI("http://u:p@www.%s:80/path" %
              u"\N{SNOWMAN}".encode('idna'))

    def test_repr(self):
        expect = "URI('http://u:p@www.xn--n3h/path', encoding='idna')".encode('ascii')
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


class TestURI(unittest.TestCase):

    def test_unicode_input_fails(self):
        self.assertRaises(TypeError, URI, u"http://www.example.com/")

    def test_iri_input(self):
        uri = TestURISnowman.uri
        iri = IRI(uri)
        self.assertEquals(str(uri), str(URI(iri)))
        self.assertEquals(unicode(uri), unicode(URI(iri)))
