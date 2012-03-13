# encoding: utf-8
import urlparse
from collections import defaultdict

import wkz_urls
import wkz_datastructures


def build_netloc(hostname, auth=None, port=None):
    return "%s%s%s" % (
        auth + '@' if auth else '',
        hostname,
        ':' + str(port) if port else ''
    )


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


class _RI(object):

    def __init__(self, ri, **kwargs):
        self.encoding = getattr(self, 'encoding', None)

        # NOTE: might be better to subclass instead of pass a query_cls around
        self.query_cls = kwargs.get('query_cls', wkz_datastructures.MultiDict)

        (self._scheme, self._auth, self._hostname, self._port, self._path,
         self._querystr, self._fragment) = wkz_urls._uri_split(ri)

    def __hash__(self):
        return hash(str(self))

    @property
    def _ri(self):
        return unsplit(netloc=self.netloc, scheme=self.scheme,
                       path=self.path, querystr=self.querystr,
                       fragment=self.fragment)

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

        new_ri = unsplit(**vals)
        return type(self)(new_ri, encoding=self.encoding, query_cls=self.query_cls)

    @property
    def update_query(self):
        raise NotImplementedError

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
            encoding = self.encoding
            querystr = self.querystr
            if isinstance(querystr, unicode):
                encoding = 'utf-8'
                querystr = querystr.encode(encoding)

            self._decoded_query = list(wkz_urls._url_decode_impl(
                querystr.split('&'), encoding,
                False, True, 'replace'
            ))
        return self.query_cls(self._decoded_query)

    @property
    def fragment(self):
        return self._fragment

    @property
    def netloc(self):
        return build_netloc(self.hostname, self.auth, self.port)

    def join(self, other):
        if not isinstance(other, type(self)):
            raise TypeError

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
            vals['querystr'] = '&'.join([('%s=%s' % (k,v)) for (k,v) in query.items()]) # TODO: do this properly

        if other.fragment:
            if self.fragment:
                raise Exception
            vals['fragment'] = other.fragment

        new_ri = unsplit(**vals)
        return type(self)(new_ri, encoding=self.encoding, query_cls=self.query_cls)


class IRI(_RI):

    def __init__(self, iri, **kwargs):

        # convert URI and str types to unicode
        if isinstance(iri, URI):
            iri = unicode(iri.to_iri())

        if not isinstance(iri, unicode):
            raise TypeError("iri must be a unicode or URI")

        # if we don't have a unicode at this point, we can't convert
        if not isinstance(iri, unicode):
            msg = "could not convert {0} to IRI: {1}"
            raise ValueError(msg.format(type(iri), iri))

        super(IRI, self).__init__(iri, **kwargs)

    def __repr__(self):
        return "IRI(%s)" % repr(unicode(self))

    def __str__(self):
        return self.encode()

    def __unicode__(self):
        return self._ri

    def encode(self, encoding='utf-8'):
        return unicode(self).encode(encoding)

    def to_uri(self):
        return URI(wkz_urls.iri_to_uri(self), encoding='idna')


class URI(_RI):

    def __init__(self, uri, encoding='ascii', **kwargs):

        if isinstance(uri, unicode):
            raise TypeError("uri must be a string or IRI")

        if isinstance(uri, IRI):
            uri = str(uri.to_uri())

        self.encoding = encoding
        super(URI, self).__init__(uri, **kwargs)

    def __repr__(self):
        return "URI(%r, encoding='%s')" % (str(self), self.encoding)

    def __str__(self):
        return self._ri

    def __unicode__(self):
        return self.decode()

    def decode(self):
        if self.encoding == 'idna':
            (scheme, auth, hostname, port, path, querystr, fragment
                ) = wkz_urls._uri_split(self._ri)
            hostname = hostname.decode('')
        return str(self).decode(self.encoding)

    def to_iri(self):
        return IRI(wkz_urls.uri_to_iri(self))
