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

    def test_convert_pile_of_poo(self):
        raise SkipTest("Not Implemented")
        iri = IRI(u"http://u:p@www.💩.la:80/path?q=arg#frag")
        try:
            URI(iri)
        except Exception as e:
            assert False, "{0} {1}".format(type(e), e)

    def test_non_existent_scheme(self):
        try:
            URI("watwatwat://wat.wat/wat")
        except Exception as e:
            assert False, "{0} {1}".format(type(e), e)

    def test_uri_from_lenient(self):
        lenient_uri = URI.from_lenient(u'http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)'.encode('utf8'))
        self.assertEquals(repr(lenient_uri), "URI('http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29')")


class TestURISnowman(cases.IdentifierCase):

    ri = URI("http://u:p@www.%s:80/path?q=arg#frag"
             % u"\N{SNOWMAN}".encode('idna'))
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


class TestURIConvertedSnowman(cases.IdentifierCase):

    iri = IRI(u"http://u:p@www.\N{SNOWMAN}:80/path?q=arg#frag")
    ri = URI(iri)
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


class TestURIPileOfPoo(cases.IdentifierCase):

    ri = URI("http://u:p@www.xn--ls8h.la:80/path?q=arg#frag")
    expect = dict(
        scheme="http",
        auth="u:p",
        hostname="www.xn--ls8h.la",
        port="80",
        path="/path",
        query=MultiDict([('q', 'arg')]),
        querystr='q=arg',
        fragment="frag",
        netloc="u:p@www.xn--ls8h.la:80",
    )


class TestURIJoin(cases.JoinAndUpdateCase):

    RI = lambda self, s: URI(self._literal_wrapper(s), encoding='utf-8')

    def _literal_wrapper(self, lit):
        return lit.encode('utf-8')

    def test_cannot_join_uri(self):
        self.assertRaises(TypeError,
                          self.RI('http://localhost:8000').join,
                          IRI(u'/path/to/file')
                         )


class TestURINormalizes(cases.NormalizeCase):

    RI = URI

    def _literal_wrapper(self, lit):
        return lit.encode('utf-8')
