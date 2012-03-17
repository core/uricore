# encoding: utf-8
from __future__ import unicode_literals
import unittest

from nose.plugins.skip import SkipTest

from uricore import IRI, URI
from uricore.wkz_datastructures import MultiDict

import cases


class TestIRIInputs(unittest.TestCase):

    def test_str_input_fails(self):
        self.assertRaises(TypeError, IRI, 'http://example.com'.encode('ascii'))

    def test_uri_input(self):
        iri = TestIRISnowman.ri
        uri = URI(iri)
        self.assertEquals(str(iri), str(IRI(uri)))
        self.assertEquals(unicode(iri), unicode(IRI(uri)))

    def test_repr(self):
        iri = TestIRISnowman.ri
        eval_iri = eval(repr(iri))
        self.assertEquals(iri, eval_iri)

    def test_idn_ascii_encoding(self):
        iri = IRI(u"http://Bücher.ch/")
        self.assertEquals(str(iri), "http://xn--bcher-kva.ch/")

    def test_idn_ascii_encoding_poo(self):
        raise SkipTest("Not Implemented")
        iri = IRI(u"http://💩.la/")
        self.assertEquals(str(iri), "http://xn--ls8h.la/")


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
    )


class TestIRIJoin(cases.JoinCase):

    RI = IRI

    def test_cannot_join_uri(self):
        self.assertRaises(TypeError,
                          IRI('http://localhost:8000').join,
                          URI(str('/path/to/file'))
                         )
