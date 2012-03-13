# encoding: utf-8
from __future__ import unicode_literals
import unittest

import cases
from resources import IRI, URI
from wkz_datastructures import MultiDict


class TestIRIInputs(unittest.TestCase):

    def test_str_input_fails(self):
        self.assertRaises(TypeError, IRI, 'http://example.com'.encode('ascii'))

    def test_uri_input(self):
        iri = TestIRISnowman.ri
        uri = URI(iri)
        self.assertEquals(str(iri), str(IRI(uri)))
        self.assertEquals(unicode(iri), unicode(IRI(uri)))


class TestIRISnowman(cases.RICase):

    ri = IRI("http://u:p@www.\N{SNOWMAN}:80/path?q=arg#frag")
    expect = dict(
        scheme="http",
        auth="u:p",
        hostname="www.\u2603",
        port="80",
        path="/path",
        query=MultiDict([('q', 'arg')]),
        querystr='q=arg',
        fragment="frag",
        netloc="u:p@www.\u2603:80",
        repr="IRI(u'http://u:p@www.\\u2603:80/path?q=arg#frag')".encode('ascii')
    )


class TestIRIJoin(cases.JoinCase):

    RI = IRI
