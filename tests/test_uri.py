# encoding: utf-8
import unittest

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
        repr="URI('http://u:p@www.xn--n3h:80/path?q=arg#frag', encoding='ascii')"
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
