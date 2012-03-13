# encoding: utf-8
import unittest

from resources import URI
from resources import IRI
from wkz_datastructures import MultiDict


class TestJoin(unittest.TestCase):

    def test_join_path_to_netloc(self):
        uri = URI('http://localhost:8000').join(URI("/path/to/file"))
        self.assertEquals(uri.scheme, 'http')
        self.assertEquals(uri.netloc, 'localhost:8000')
        self.assertEquals(uri.path, '/path/to/file')

    def test_join_path_to_path(self):
        uri = URI('http://localhost:8000/here/is/the').join(URI("/path/to/file"))
        self.assertEquals(uri.scheme, 'http')
        self.assertEquals(uri.netloc, 'localhost:8000')
        self.assertEquals(uri.path, '/here/is/the/path/to/file')

    def test_join_fragment_and_path(self):
        uri = URI('http://localhost:8000/here/is/the').join(URI("/thing#fragment"))
        self.assertEquals(uri.path, '/here/is/the/thing')
        self.assertEquals(uri.fragment, 'fragment')

    def test_join_query_to_path(self):
        uri = URI('http://localhost:8000/path/to/file').join(URI("?yes=no&left=right"))
        self.assertEquals(uri.path, '/path/to/file')
        self.assertEquals(uri.query, MultiDict(dict(yes='no', left='right')))
        self.assertEquals(uri.querystr, 'yes=no&left=right')

    def test_join_query_to_query(self):
        uri = URI('http://localhost:8000/path/to/file?yes=no').join(URI("?left=right"))
        self.assertEquals(uri.path, '/path/to/file')
        self.assertEquals(uri.query, MultiDict(dict(yes='no', left='right')))
        self.assertEquals(uri.querystr, 'yes=no&left=right')

    def test_join_fragment_to_query(self):
        uri = URI('http://rubberchick.en/path/to/file?yes=no').join(URI("#giblets"))
        self.assertEquals(uri.path, '/path/to/file')
        self.assertEquals(uri.query, MultiDict(dict(yes='no', left='right')))
        self.assertEquals(uri.querystr, 'yes=no')
        self.assertEquals(uri.fragment, 'giblets')
