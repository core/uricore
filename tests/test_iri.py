# encoding: utf-8
from __future__ import unicode_literals
import unittest

from resources import IRI

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
