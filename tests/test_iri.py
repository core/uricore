# encoding: utf-8
from __future__ import unicode_literals
import unittest

from nose.plugins.skip import SkipTest

from uricore import IRI, URI
from uricore.wkz_datastructures import MultiDict

import cases


class TestIRI(unittest.TestCase):

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
        iri = IRI("http://Bücher.ch/")
        self.assertEquals(str(iri), "http://xn--bcher-kva.ch/")

    def test_convert_pile_of_poo(self):
        raise SkipTest("Not Implemented")
        uri = URI("http://u:p@www.xn--ls8h.la:80/path?q=arg#frag".encode('utf-8'))
        try:
            IRI(uri)
        except Exception as e:
            assert False, "{0} {1}".format(type(e), e)

    def test_non_existent_scheme(self):
        try:
            IRI("watwatwat://wat.wat/wat")
        except Exception as e:
            assert False, "{0} {1}".format(type(e), e)

    def test_nonascii_query_keys(self):
        IRI(u'http://example.com/?gro\xdf=great')

    def test_iri_from_lenient(self):
        lenient_iri = IRI.from_lenient(u'http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)')
        self.assertEquals(repr(lenient_iri), "IRI(u'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29')")


class TestIRISnowman(cases.IdentifierCase):

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


class TestIRIConvertedSnowman(cases.IdentifierCase):

    uri = URI(("http://u:p@www.%s:80/path?q=arg#frag"
               % u"\N{SNOWMAN}".encode('idna')).encode('utf-8'))
    ri = IRI(uri)
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


class TestIRIPileOfPoo(cases.IdentifierCase):

    ri = IRI("http://u:p@www.💩.la:80/path?q=arg#frag")
    expect = dict(
        scheme="http",
        auth="u:p",
        hostname="www.💩.la",
        port="80",
        path="/path",
        query=MultiDict([('q', 'arg')]),
        querystr='q=arg',
        fragment="frag",
        netloc="u:p@www.💩.la:80",
    )


class TestIRIIPv6(cases.IdentifierCase):

    ri = IRI("http://u:p@[2a00:1450:4001:c01::67]/path?q=arg#frag")
    expect = dict(
        scheme="http",
        auth="u:p",
        hostname="2a00:1450:4001:c01::67",
        port=None,
        path="/path",
        query=MultiDict([('q', 'arg')]),
        querystr='q=arg',
        fragment="frag",
        netloc="u:p@[2a00:1450:4001:c01::67]",
    )


class TestIRIIPv6WithPort(cases.IdentifierCase):

    ri = IRI("http://u:p@[2a00:1450:4001:c01::67]:80/path?q=arg#frag")
    expect = dict(
        scheme="http",
        auth="u:p",
        hostname="2a00:1450:4001:c01::67",
        port="80",
        path="/path",
        query=MultiDict([('q', 'arg')]),
        querystr='q=arg',
        fragment="frag",
        netloc="u:p@[2a00:1450:4001:c01::67]:80",
    )


class TestIRIJoin(cases.JoinAndUpdateCase):

    RI = IRI

    def test_cannot_join_uri(self):
        self.assertRaises(TypeError,
                          IRI('http://localhost:8000').join,
                          URI(str('/path/to/file'))
                         )


class TestIRINormalizes(cases.NormalizeCase):

    RI = IRI
