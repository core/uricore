# encoding: utf-8

import unittest
import resources

class TestInterface(unittest.TestCase):

    def setUp(self):
        self.fixture = resources.Resource("http://example.com")

    def test_copy_on_update(self):
        url2 = self.fixture.update(scheme="https")
        self.assertNotEquals(self.fixture, url2)

    def test_punycode(self):
        ascii_url = 'http://xn--ls8h.la/'
        url = resources.Resource(u"http://💩.la/")
        self.assertEquals(url.to_ascii(), ascii_url)

    def test_getattr(self):
        self.assertEquals(self.fixture.scheme, 'http')

    def test_setattr(self):
        self.assertRaises(AttributeError, setattr, self.fixture.scheme, "")
