# encoding: utf-8
from __future__ import unicode_literals
import wkz_urls


class _RI(object):

    def __init__(self, query_class=None):
        self.decoder


class IRI(_RI):

    def __init__(self, iri, charset='utf-8', query_class=None):
        super(IRI, self).__init__(query_class)
        if isinstance(iri, URI):
            iri = iri.to_iri().to_unicode()
        self.iri = iri

    def to_uri(self):
        return URI(wkz_urls.iri_to_uri(self.iri))

    def to_unicode(self):
        return unicode(self.iri)


class URI(_RI):

    def __init__(self, uri, query_class=None):
        super(URI, self).__init__(query_class)
        if isinstance(uri, IRI):
            uri = uri.to_uri().to_string()
        self.uri = uri

    def to_iri(self):
        return IRI(wkz_urls.uri_to_iri(self.uri))

    def to_string(self):
        return str(self.uri)
