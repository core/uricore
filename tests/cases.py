# encoding: utf-8
from __future__ import unicode_literals
import unittest

from uricore.wkz_datastructures import MultiDict


class RICase(unittest.TestCase):
    # Test properties and representations
    #
    # Class variables:
    # ri = URI or IRI object
    # expect = dict of expected results

    def test_scheme_baby(self):
        self.assertEquals(self.ri.scheme, self.expect['scheme'])

    def test_auth(self):
        self.assertEquals(self.ri.auth, self.expect['auth'])

    def test_hostname(self):
        self.assertEquals(self.ri.hostname, self.expect['hostname'])

    def test_port(self):
        self.assertEquals(self.ri.port, self.expect['port'])

    def test_path(self):
        self.assertEquals(self.ri.path, self.expect['path'])

    def test_query(self):
        self.assertEquals(self.ri.query, self.expect['query'])

    def test_querystr(self):
        self.assertEquals(self.ri.querystr, self.expect['querystr'])

    def test_fragment(self):
        self.assertEquals(self.ri.fragment, self.expect['fragment'])

    def test_netloc(self):
        self.assertEquals(self.ri.netloc, self.expect['netloc'])

    def test_repr(self):
        self.assertEquals(repr(self.ri), self.expect['repr'])


class JoinCase(unittest.TestCase):
    # Test join
    #
    # Class variables:
    # RI = IRI/URI constructor given a unicode object

    def test_join_path_to_netloc(self):
        ri = self.RI('http://localhost:8000').join(self.RI('/path/to/file'))
        self.assertEquals(ri.scheme, 'http')
        self.assertEquals(ri.netloc, 'localhost:8000')
        self.assertEquals(ri.path, '/path/to/file')

    def test_join_path_to_path(self):
        ri = self.RI('http://localhost:8000/here/is/the').join(self.RI('/path/to/file'))
        self.assertEquals(ri.scheme, 'http')
        self.assertEquals(ri.netloc, 'localhost:8000')
        self.assertEquals(ri.path, '/here/is/the/path/to/file')

    def test_join_fragment_and_path(self):
        ri = self.RI('http://localhost:8000/here/is/the').join(self.RI('/thing#fragment'))
        self.assertEquals(ri.path, '/here/is/the/thing')
        self.assertEquals(ri.fragment, 'fragment')

    def test_join_query_to_path(self):
        ri = self.RI('http://localhost:8000/path/to/file').join(self.RI('?yes=no&left=right'))
        self.assertEquals(ri.path, '/path/to/file')
        self.assertEquals(ri.query, MultiDict(dict(yes='no', left='right')))
        self.assertEquals(ri.querystr, 'yes=no&left=right')

    def test_join_query_to_query(self):
        ri = self.RI('http://localhost:8000/path/to/file?yes=no').join(self.RI('?left=right'))
        self.assertEquals(ri.path, '/path/to/file')
        self.assertEquals(ri.query, MultiDict(dict(yes='no', left='right')))
        self.assertEquals(ri.querystr, 'yes=no&left=right')

    def test_join_query_to_query_to_make_multi_query(self):
        ri = self.RI('http://localhost:8000/path/to/file?yes=no').join(self.RI('?yes=maybe&left=right'))
        self.assertEquals(ri.path, '/path/to/file')
        self.assertEquals(ri.query, MultiDict([('yes','no'), ('yes','maybe'), ('left','right'),]))
        self.assertEquals(ri.querystr, 'yes=no&yes=maybe&left=right')

    def test_join_fragment_to_query(self):
        ri = self.RI('http://rubberchick.en/path/to/file?yes=no').join(self.RI('#giblets'))
        self.assertEquals(ri.path, '/path/to/file')
        self.assertEquals(ri.query, MultiDict(dict(yes='no',)))
        self.assertEquals(ri.querystr, 'yes=no')
        self.assertEquals(ri.fragment, 'giblets')

    def test_join_with_literal_fails(self):
        ri = self.RI('https://secure.pants.net/')
        self.assertRaises(TypeError, ri.join, '/path/to/thing')

    def test_join_scheme_with_path(self):
        ri = self.RI('gopher://')
        result = ri.join(self.RI('nowhere'))
        self.assertEquals(result.scheme, 'gopher')
        self.assertEquals(result.path, '/nowhere')

    def test_join_no_hostname_with_hostname(self):
        ri = self.RI('gopher://')
        result = ri.join(self.RI('//whole.org/ville'))
        self.assertEquals(result.scheme, 'gopher')
        self.assertEquals(result.hostname, 'whole.org')
        self.assertEquals(result.path, '/ville')
