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
        self.encoding = kwargs.get('encoding')
        #NOTE: might be better to subclass instead of pass a query_cls around
        self.query_cls = kwargs.get('query_cls', wkz_datastructures.MultiDict)

        (self._scheme, self._auth, self._hostname, self._port, self._path,
         self._querystr, self._fragment) = wkz_urls._uri_split(ri)

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
        pass

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

        encoding = self.encoding
        querystr = self.querystr
        if isinstance(querystr, unicode):
            encoding = 'utf-8'
            querystr = querystr.encode(encoding)

        if not hasattr(self, '_decoded_query'):
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

    @property
    def ri(self):
        return unsplit(netloc=self.netloc, scheme=self.scheme,
                       path=self.path, querystr=self.querystr,
                       fragment=self.fragment)


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
        return "IRI(%s)" % str(self)

    def __str__(self):
        return repr(unicode(self))

    def __unicode__(self):
        return self.ri

    def to_uri(self):
        return URI(wkz_urls.iri_to_uri(self))


class URI(_RI):

    def __init__(self, uri, encoding='utf-8', **kwargs):

        if isinstance(uri, unicode):
            raise TypeError("uri must be a string or IRI")

        if isinstance(uri, IRI):
            uri = str(uri.to_uri())

        super(URI, self).__init__(uri, encoding=encoding, **kwargs)

    def __repr__(self):
        return "URI(%s, encoding='idna')" % repr(str(self))

    def __str__(self):
        return self.ri

    def __unicode__(self):
        return unicode(str(self))

    def to_iri(self):
        return IRI(wkz_urls.uri_to_iri(self))
