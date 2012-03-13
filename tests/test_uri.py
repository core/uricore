# encoding: utf-8
import unittest

from resources import URI
from resources import IRI


class TestURISnowman(unittest.TestCase):

    def setUp(self):
        idna = u"\N{SNOWMAN}".encode('idna')
        uri = "http://u:p@www.%s:80/path" % idna
        self.uri = URI(uri)

    def testFail(self):
        self.assertRaises(TypeError, URI, u"http://\u2603/")

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
