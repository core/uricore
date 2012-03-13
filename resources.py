# encoding: utf-8
from __future__ import unicode_literals

import urlparse
from collections import namedtuple

import wkz_urls


class _RI(object):
    RIComponents = namedtuple('RIComponents', ('scheme', 'auth', 'hostname',
                                               'port', 'path', 'querystr',
                                               'query', 'fragment'))

    def __init__(self, ri, encoding, query_class=None):
        scheme, auth, hostname, port, path, querystr, fragment = (
            wkz_urls._uri_split(ri))

        query = wkz_urls.url_decode(querystr, encoding, cls=query_class)
        self.components = self.RIComponents(scheme, auth, hostname, port, path,
                                            querystr, query, fragment)

    def _unsplit(self):
        return urlparse.urlunsplit((
            self.scheme, self.hostname,
            self.path, self.querystr,
            self.fragment
        ))

    @property
    def scheme(self):
        return self.components.scheme

    @property
    def auth(self):
        return self.components.auth

    @property
    def hostname(self):
        return self.components.hostname

    @property
    def port(self):
        return self.components.port

    @property
    def path(self):
        return self.components.path

    @property
    def querystr(self):
        return self.components.querystr

    @property
    def query(self):
        return self.components.query

    @property
    def fragment(self):
        return self.components.fragment

    def __repr__(self):
        return "%s(%r, encoding='idna')" % (self.__class__.__name__, str(self))


class IRI(_RI):
    default_encoding = 'utf8'

    def __init__(self, iri, encoding=None, query_class=None):

        # convert URI and str types to unicode
        if isinstance(iri, URI):
            iri = unicode(iri.to_iri())
        elif isinstance(iri, str):
            iri = iri.decode(encoding=encoding or self.default_encoding)
        elif isinstance(iri, unicode) and encoding is not None:
            raise ValueError("encoding must be None if iri is unicode")

        # if we don't have a unicode at this point, we can't convert
        if not isinstance(iri, unicode):
            msg = "could not convert {0} to IRI: {1}"
            raise ValueError(msg.format(type(iri), iri))

        super(IRI, self).__init__(iri, encoding or self.default_encoding, query_class=query_class)

    def __unicode__(self):
        return self._unsplit()

    def __str__(self):
        return str(self.to_uri())

    def to_uri(self):
        return URI(wkz_urls.iri_to_uri(self))


class URI(_RI):

    def __init__(self, uri, query_class=None):
        if isinstance(uri, IRI):
            uri = str(uri.to_uri())
        super(URI, self).__init__(uri, 'ascii', query_class=query_class)

    def __str__(self):
        return self._unsplit()

    def __unicode__(self):
        return unicode(self.to_iri())

    def to_iri(self):
        return IRI(wkz_urls.uri_to_iri(str(self)))
