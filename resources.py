# encoding: utf-8
from __future__ import unicode_literals
from wkz_datastructures import MultiDict # TODO: should be from httpcore.datastructures
import wkz_urls


class _RI(object):
    RIComponents = namedtuple('RIComponents', ('scheme', 'auth', 'hostname',
                                               'port', 'path', 'querystr',
                                               'query', 'fragment'))

    def __init__(self, ri, charset, query_class=None):
        if query_class is None:
            query_class = MultiDict
        scheme, auth, hostname, port, path, querystr, fragment = wkz_urls._uri_split(ri)

        query = wkz_urls.url_decode(querystr, charset, cls=query_class)
        self.components = RIComponents(scheme, auth, hostname, port, path,
                                       querystr, query, fragment)


class IRI(_RI):

    def __init__(self, iri, charset='utf-8', query_class=None):
        super(IRI, self).__init__(iri, charset, query_class=query_class)
        if isinstance(iri, URI):
            iri = iri.to_iri().to_unicode()

        self.pieces = wkz_urls._uri_split(c

    def to_uri(self):
        return URI(wkz_urls.iri_to_uri(self.iri))

    def to_unicode(self):
        return unicode(self.iri)


class URI(_RI):

    def __init__(self, uri, query_class=None):
        super(URI, self).__init__(query_class=query_class)
        if isinstance(uri, IRI):
            uri = uri.to_uri().to_string()
        self.uri = uri

    def to_iri(self):
        return IRI(wkz_urls.uri_to_iri(self.uri))

    def to_string(self):
        return str(self.uri)
