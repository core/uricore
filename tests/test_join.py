# encoding: utf-8
import unittest

from resources import URI
from resources import IRI
from wkz_datastructures import MultiDict


class TestJoin(unittest.TestCase):

    def test_join_path_to_netloc(self):
        uri = URI('http://localhost:8000').join(URI("/path/to/file"))
        assert uri.scheme == 'http'
        assert uri.netloc == 'localhost:8000'
        assert uri.path == '/path/to/file'

    def test_join_path_to_path(self):
        uri = URI('http://localhost:8000/here/is/the').join(URI("/path/to/file"))
        assert uri.scheme == 'http'
        assert uri.netloc == 'localhost:8000'
        assert uri.path == '/here/is/the/path/to/file'

    def test_join_fragment_and_path(self):
        uri = URI('http://localhost:8000/here/is/the').join(URI("/thing#fragment"))
        assert uri.path == '/here/is/the/thing'
        assert uri.fragment = 'fragment'

    def test_join_query_to_path(self):
        uri = URI('http://localhost:8000/path/to/file').join(URI("?yes=no&left=right"))
        assert uri.path == '/path/to/file'
        assert uri.query == MultiDict(dict(yes='no', left='right'))
        assert uri.querystr == 'yes=no&left=right'

    def test_join_query_to_query(self):
        uri = URI('http://localhost:8000/path/to/file?yes=no').join(URI("?left=right"))
        assert uri.path == '/path/to/file'
        assert uri.query == MultiDict(dict(yes='no', left='right'))
        assert uri.querystr == 'yes=no&left=right'

    def test_join_fragment_to_query(self):
        uri = URI('http://rubberchick.en/path/to/file?yes=no').join(URI("#giblets"))
        assert uri.path == '/path/to/file'
        assert uri.query == MultiDict(dict(yes='no', left='right'))
        assert uri.querystr == 'yes=no'
        assert uri.fragment = 'giblets'
