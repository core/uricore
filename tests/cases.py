import unittest


class RICase(unittest.TestCase):

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
        raise NotImplementedError("make test!!1!")
        #self.assertEquals(self.ri.query, self.expect['query'])

    def test_querystr(self):
        raise NotImplementedError("make test!!1!")
        #self.assertEquals(self.ri.querystr, self.expect['querystr'])

    def test_fragment(self):
        self.assertEquals(self.ri.fragment, self.expect['fragment'])

    def test_netloc(self):
        self.assertEquals(self.ri.netloc, self.expect['netloc'])

    def test_repr(self):
        self.assertEquals(repr(self.ri), self.expect['repr'])
