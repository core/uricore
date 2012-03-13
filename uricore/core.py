# encoding: utf-8
from __future__ import unicode_literals

import urlparse
from collections import defaultdict

from . import wkz_urls  # temporary module name
from . import wkz_datastructures  # temporary module name


def build_netloc(hostname, auth=None, port=None):
    auth = "{0}@".format(auth) if auth else ""
    port = ":{0}".format(port) if port else ""
    return "{0}{1}{2}".format(auth, hostname, port)


def unsplit(**kwargs):
    parts = defaultdict(str)
    for k in kwargs:
        if kwargs[k]:
            parts[k] = kwargs[k]

    if 'netloc' in parts:
        netloc = parts['netloc']
    else:
        netloc = build_netloc(parts['hostname'], parts.get('auth'),
                              parts.get('port'))

    return urlparse.urlunsplit((
        parts['scheme'], netloc,
        parts['path'], parts['querystr'],
        parts['fragment']
    ))


class IRI(object):

    def __init__(self, iri, query_cls=None):

        if isinstance(iri, (URI, IRI)):  # TODO: don't make a new copy
            iri = unicode(iri)

        if not isinstance(iri, unicode):
            raise TypeError("iri must be a unicode or IRI/URI: %s" % type(iri))

        # if we don't have a unicode at this point, we can't convert
        if not isinstance(iri, unicode):
            msg = "could not convert {0} to IRI: {1}"
            raise ValueError(msg.format(type(iri), iri))

        (self._scheme,
         self._auth,
         self._hostname,
         self._port,
         self._path,
         self._querystr,
         self._fragment) = wkz_urls._uri_split(iri)

        # NOTE: might be better to subclass instead of pass a query_cls around
        self.query_cls = query_cls or wkz_datastructures.MultiDict

    def __repr__(self):
        return "IRI({0!r})".format(unicode(self)).encode('ascii')

    def __str__(self):
        return self.encode()

    def __unicode__(self):
        return unsplit(netloc=self.netloc, scheme=self.scheme,
                       path=self.path, querystr=self.querystr,
                       fragment=self.fragment)

    def __hash__(self):
        return hash(str(self))

    def encode(self, encoding='utf-8'):
        return unicode(self).encode(encoding)

    def to_uri(self):
        return URI(wkz_urls.iri_to_uri(self), encoding='idna')

    @property
    def scheme(self):
        return self._scheme

    @property
    def auth(self):
        return self._auth

    @property
    def hostname(self):
        return self._hostname

    @property
    def port(self):
        return self._port

    @property
    def path(self):
        return self._path

    @property
    def querystr(self):
        return self._querystr

    @property
    def query(self):
        """Return a new instance of query_cls."""

        if not hasattr(self, '_decoded_query'):
            self._decoded_query = list(wkz_urls._url_decode_impl(
                self.querystr.encode('utf-8').split('&'.encode('utf-8')),
                'utf-8', False, True, 'strict'))
        return self.query_cls(self._decoded_query)

    @property
    def fragment(self):
        return self._fragment

    @property
    def netloc(self):
        return build_netloc(self.hostname, self.auth, self.port)

    def update(self, **kwargs):
        vals = {
            'scheme': self.scheme,
            'auth': self.auth,
            'hostname': self.hostname,
            'port': self.port,
            'path': self.path,
            'querystr': self.querystr,
            'fragment': self.fragment
        }
        if len(kwargs):
            vals.update(kwargs)

        return type(self)(unsplit(**vals), query_cls=self.query_cls)

    def update_query(self):
        raise NotImplementedError

    def join(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(type(self))

        # BUG: if only one of the two IRIs being joined have these set,
        #      these shouldn't get raised
        if not self.scheme or not self.hostname:
            raise Exception # TODO: better errors
        if other.scheme or other.hostname:
            raise Exception

        vals = {
            'scheme': self.scheme,
            'auth': self.auth,
            'hostname': self.hostname,
            'port': self.port,
            'path': self.path,
            'querystr': self.querystr,
            'fragment': self.fragment,
        }

        if other.path:
            if self.querystr or self.fragment:
                raise Exception
            vals['path'] = '/'.join([self.path, other.path]).replace('//', '/')

        if other.querystr:
            if self.fragment:
                raise Exception
            query = self.query
            query.update(other.query)
            vals['querystr'] = '&'.join([('%s=%s' % (k, v)) for (k, v) in query.items()])  # TODO: do this properly

        if other.fragment:
            if self.fragment:
                raise Exception
            vals['fragment'] = other.fragment

        return type(self)(unsplit(**vals), query_cls=self.query_cls)


class URI(object):

    def __init__(self, uri, encoding='utf-8'):

        if isinstance(uri, str):
            self._iri = IRI(uri.decode(encoding))
        elif isinstance(uri, IRI):
            self._iri = IRI(uri)
        else:
            raise TypeError("uri must be a string or IRI: %s", type(uri))

        self.encoding = encoding

    def __getattr__(self, name):
        return getattr(self._iri, name)

    def __repr__(self):
        return "URI(%r, encoding='%s')" % (str(self), self.encoding)

    def __str__(self):
        return self._iri.encode(encoding=self.encoding)

    def __unicode__(self):
        return unicode(self._iri)

    def join(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(type(self))

        iri = self._iri.join(IRI(other))
        return URI(iri)

    def to_iri(self):
        return IRI(wkz_urls.uri_to_iri(self))
