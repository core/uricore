# encoding: utf-8
from __future__ import unicode_literals
from collections import namedtuple
import urlparse
import wkz_urls


class _RI(object):
    RIComponents = namedtuple('RIComponents', ('scheme', 'auth', 'hostname',
                                               'port', 'path', 'querystr',
                                               'query', 'fragment'))

    def __init__(self, ri, charset, query_class=None):
        scheme, auth, hostname, port, path, querystr, fragment = wkz_urls._uri_split(ri)

        query = wkz_urls.url_decode(querystr, charset, cls=query_class)
        self.components = self.RIComponents(scheme, auth, hostname, port, path,
                                       querystr, query, fragment)

    @property
    def ri_components(self):
        return (self.components.scheme, self.components.hostname,
                self.components.path, self.components.querystr,
                self.components.fragment)


class IRI(_RI):

    def __init__(self, iri, charset='utf-8', query_class=None):
        if isinstance(iri, URI):
            iri = iri.to_iri().to_unicode()
        super(IRI, self).__init__(iri, charset, query_class=query_class)

    def to_uri(self):
        return URI(wkz_urls.iri_to_uri(self.to_unicode()))

    def to_unicode(self):
        return unicode(urlparse.urlunsplit(self.ri_components))

    def __repr__(self):
        return "IRI(%s)" % repr(self.to_unicode())


class URI(_RI):

    def __init__(self, uri, query_class=None):
        if isinstance(uri, IRI):
            uri = uri.to_uri().to_string()
        super(URI, self).__init__(uri, 'ascii', query_class=query_class)

    def to_iri(self):
        return IRI(wkz_urls.uri_to_iri(self.to_string()))

    def to_string(self):
        return str(urlparse.urlunsplit(self.ri_components))

    def __repr__(self):
        return "URI(%s)" % repr(self.to_string())
