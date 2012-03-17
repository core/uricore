# encoding: utf-8
import unittest

from nose.plugins.skip import SkipTest

from uricore import IRI, URI
from uricore.wkz_datastructures import MultiDict

import cases


class TestURI(unittest.TestCase):

    def test_unicode_input_fails(self):
        self.assertRaises(TypeError, URI, u"http://www.example.com/")

    def test_iri_input(self):
        uri = TestURISnowman.ri
        iri = IRI(uri)
        self.assertEquals(str(uri), str(URI(iri)))
        self.assertEquals(unicode(uri), unicode(URI(iri)))

    def test_repr(self):
        uri = TestURISnowman.ri
        eval_uri = eval(repr(uri))
        self.assertEquals(uri, eval_uri)

    def test_idn_ascii_encoding(self):
        uri = URI(u"http://Bücher.ch/".encode('utf-8'))
        self.assertEquals(str(uri), "http://xn--bcher-kva.ch/")

    def test_idn_ascii_encoding_poo(self):
        raise SkipTest("Not Implemented")
        uri = URI(u"http://💩.la/".encode('utf-8'))
        self.assertEquals(str(uri), "http://xn--ls8h.la/")


class TestURISnowman(cases.RICase):

    ri = URI("http://u:p@www.%s:80/path?q=arg#frag" %
             u"\N{SNOWMAN}".encode('idna'), encoding='ascii')
    expect = dict(
        scheme="http",
        auth="u:p",
        hostname="www.xn--n3h",
        port="80",
        path="/path",
        query=MultiDict([('q', 'arg')]),
        querystr='q=arg',
        fragment="frag",
        netloc="u:p@www.xn--n3h:80",
    )


class TestURIJoin(cases.JoinCase):

    RI = lambda self, s: URI(self._literal_wrapper(s), encoding='utf-8')

    def _literal_wrapper(self, lit):
        return lit.encode('utf-8')

    def test_cannot_join_uri(self):
        self.assertRaises(TypeError,
                          self.RI('http://localhost:8000').join,
                          IRI(u'/path/to/file')
                         )
