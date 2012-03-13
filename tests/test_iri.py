# encoding: utf-8
from __future__ import unicode_literals

import unittest

from resources import IRI, URI


class TestIRISnowman(unittest.TestCase):

    iri = IRI("http://u:p@www.\N{SNOWMAN}:80/path")

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


class TestIRI(unittest.TestCase):

    def test_str_input_fails(self):
        self.assertRaises(TypeError, IRI, 'http://example.com'.encode('ascii'))

    def test_uri_input(self):
        iri = TestIRISnowman.iri
        uri = URI(iri)
        self.assertEquals(str(iri), str(IRI(uri)))
        self.assertEquals(unicode(iri), unicode(IRI(uri)))
