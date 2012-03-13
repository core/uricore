# encoding: utf-8
import urlparse

import wkz_urls
import wkz_datastructures


class _RI(object):

    def __init__(self, ri, encoding=None, query_cls=None):
        self.encoding = encoding
        #NOTE: might be better to subclass instead of pass a query_cls around
        if query_cls is None:
            query_cls = wkz_datastructures.MultiDict
        self.query_cls = query_cls

        (self._scheme, self._auth, self._hostname, self._port, self._path,
         self._querystr, self._fragment) = wkz_urls._uri_split(ri)

    def __copy__(self):
        return type(self)(ri, self.encoding, self.query_cls)

    def replace(self, attribute, value):
        attributes = ('auth', 'scheme', 'hostname', 'port', 'path', 'fragment')
        return type(self)(ri, self.encoding, self.query_cls)

    def update(self, **kwargs):
        vals = {
            'scheme': self.scheme,
            'hostname': self.hostname,
            'path': self.path,
            'querystr': self.querystr,
            'fragment': self.fragment
        }.update(kwargs)

        new_ri = urlparse.urlunsplit((
            vals['scheme'], vals['hostname'],
            vals['self.path'], vals['querystr'],
            vals['fragment']
        ))
        return type(self)(new_ri, self.encoding, self.query_cls)

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

        if not hasattr(self, '_decoded_query'):
            self._decoded_query = list(wkz_urls._url_decode_impl(
                str(self.querystr).split('&'), self.encoding,
                False, True, 'replace'
            ))
        return self.query_cls(self._decoded_query)

    @property
    def fragment(self):
        return self._fragment

    @property
    def netloc(self):
        return "%s%s%s" % (
            self.auth + '@' if self.auth else '',
            self.hostname,
            ':' + self.port if self.port else ''
        )

    def _unsplit(self):
        return urlparse.urlunsplit((
            self.scheme, self.netloc,
            self.path, self.querystr,
            self.fragment
        ))


class IRI(_RI):

    def __init__(self, iri, query_cls=None):

        # convert URI and str types to unicode
        if isinstance(iri, URI):
            iri = unicode(iri.to_iri())

        if not isinstance(iri, unicode):
            raise TypeError("iri must be a unicode or URI")

        # if we don't have a unicode at this point, we can't convert
        if not isinstance(iri, unicode):
            msg = "could not convert {0} to IRI: {1}"
            raise ValueError(msg.format(type(iri), iri))

        super(IRI, self).__init__(iri, query_cls=query_cls)

    def __repr__(self):
        return "IRI(%s)" % str(self)

    def __str__(self):
        return repr(unicode(self))

    def __unicode__(self):
        return self._unsplit()

    def to_uri(self):
        return URI(wkz_urls.iri_to_uri(self))


class URI(_RI):

    def __init__(self, uri, encoding='utf-8', query_cls=None):
        if isinstance(uri, unicode):
            raise TypeError("uri must be a string or IRI")

        if isinstance(uri, IRI):
            uri = str(uri.to_uri())

        super(URI, self).__init__(uri, encoding, query_cls=query_cls)

    def __str__(self):
        return self._unsplit()

    def __unicode__(self):
        return unicode(self.to_iri())

    def to_iri(self):
        return IRI(wkz_urls.uri_to_iri(str(self)))
