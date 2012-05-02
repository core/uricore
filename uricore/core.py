# encoding: utf-8
__all__ = ['IRI', 'URI']

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from collections import defaultdict
from template import uri_template

# TODO: import these from httpcore someday
from . import wkz_urls as urls
from . import wkz_datastructures as datastructures


def build_netloc(hostname, auth=None, port=None):
    auth = "{0}@".format(auth) if auth else ""
    port = ":{0}".format(port) if port else ""
    if isinstance(hostname, unicode):
        return u"{0}{1}{2}".format(auth, hostname, port)
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


def identifier_to_dict(identifier):
    fields = ('scheme', 'auth', 'hostname', 'port',
              'path', 'querystr', 'fragment')
    values = urls._uri_split(identifier)
    d = dict(zip(fields, values))

    # querystr is a str
    if isinstance(d['querystr'], unicode):
        d['querystr'] = d['querystr'].encode('utf-8')

    return d


class ResourceIdentifier(object):

    def __init__(self, identifier, query_cls=None):
        if not isinstance(identifier, basestring):
            raise TypeError("Expected str or unicode: %s", type(identifier))

        self._parts = identifier_to_dict(identifier)
        self._identifier = unsplit(**self._parts)

        # NOTE: might be better to subclass instead of pass a query_cls around
        self.query_cls = query_cls or datastructures.MultiDict

    def __repr__(self):
        return "{0}({1!r})".format(type(self).__name__, self._identifier)

    def __eq__(self, other):
        if set(self._parts.keys()) != set(other._parts.keys()):
            return False
        return all(self._parts[k] == other._parts[k] for k in self._parts.iterkeys())

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._identifier)

    @property
    def scheme(self):
        return self._parts['scheme']

    @property
    def auth(self):
        return self._parts['auth']

    @property
    def hostname(self):
        return self._parts['hostname']

    @property
    def port(self):
        return self._parts['port']

    @property
    def path(self):
        return self._parts['path']

    @property
    def querystr(self):
        return self._parts['querystr']

    @property
    def query(self):
        """Return a new instance of query_cls."""

        if not hasattr(self, '_decoded_query'):
            self._decoded_query = list(urls._url_decode_impl(
                self.querystr.split('&'), 'utf-8', False, True, 'strict'))
        return self.query_cls(self._decoded_query)

    @property
    def fragment(self):
        return self._parts['fragment']

    @property
    def netloc(self):
        return build_netloc(self.hostname, self.auth, self.port)

    def update(self, **kwargs):
        vals = dict(self._parts)
        if len(kwargs):
            vals.update(kwargs)

        return type(self)(unsplit(**vals), query_cls=self.query_cls)

    def update_query(self, qry):
        assert isinstance(qry, self.query_cls)

        vals = dict(self._parts)
        q = self.query
        q.update(qry)
        vals['querystr'] = urls.url_encode(q, encode_keys=True, charset=getattr(self, 'encoding', 'utf-8'))

        return type(self)(unsplit(**vals), query_cls=self.query_cls)

    def join(self, other):
        if isinstance(other, unicode):
            other = IRI(other)
        elif isinstance(other, str):
            other = URI(other)

        if not isinstance(other, type(self)):
            raise TypeError("Expected unicode or {0}: {1}".format(
                type(self).__name__, type(other).__name__))

        vals = dict(self._parts)

        if other.scheme:
            if self.scheme:
                raise ValueError("cannot join scheme onto %ss with scheme" %
                                 self.__class__.name)
            vals['scheme'] = other.scheme

        if other.auth:
            if self.auth:
                raise ValueError("cannot join auth onto %ss with auth" %
                                 self.__class__.name)
            vals['auth'] = other.auth

        if other.hostname:
            if self.hostname:
                raise ValueError(
                    "cannot join hostname onto %ss with hostname" %
                    self.__class__.name)
            vals['hostname'] = other.hostname
            vals['port'] = other.port

        if other.path:
            if self.querystr or self.fragment:
                raise ValueError(
                    "cannot join path onto %ss with querystr or fragment" %
                    self.__class__.name)
            vals['path'] = '/'.join([self.path, other.path]).replace('//', '/')

        if other.querystr:
            if self.fragment:
                raise ValueError(
                    "cannot join querystr onto %ss with fragment" %
                    self.__class__.name)
            query = self.query
            query.update(other.query)
            vals['querystr'] = urls.url_encode(query, encode_keys=True, charset=getattr(self, 'encoding', 'utf-8'))

        if other.fragment:
            if self.fragment:
                raise ValueError(
                    "cannot join fragment onto %ss with fragment" %
                    self.__class__.name)
            vals['fragment'] = other.fragment

        return type(self)(unsplit(**vals), query_cls=self.query_cls)

    @classmethod
    def from_template(cls, template, **kwargs):
        return cls(urls.url_unquote(uri_template(template, **kwargs)))



class IRI(ResourceIdentifier):

    def __init__(self, iri, query_cls=None):

        if isinstance(iri, unicode):
            identifier = iri
        elif isinstance(iri, ResourceIdentifier):
            identifier = unicode(iri)
        else:
            raise TypeError("iri must be unicode or IRI/URI: %s"
                            % type(iri).__name__)

        super(IRI, self).__init__(identifier, query_cls)

    def __str__(self):
        return urls.iri_to_uri(self._identifier)

    def __unicode__(self):
        return self._identifier

    @classmethod
    def from_lenient(cls, maybe_gibberish):
        return cls(urls.url_fix(maybe_gibberish.encode('utf-8')).decode('utf-8'))


class URI(ResourceIdentifier):

    def __init__(self, uri, encoding='utf-8', query_cls=None):

        if isinstance(uri, str):
            identifier = urls.iri_to_uri(uri.decode(encoding))
        elif isinstance(uri, ResourceIdentifier):
            identifier = str(uri)
        else:
            raise TypeError("uri must be str or IRI/URI: %s"
                            % type(uri).__name__)

        super(URI, self).__init__(identifier, query_cls)
        self.encoding = encoding

    def __str__(self):
        return self._identifier

    def __unicode__(self):
        return urls.uri_to_iri(self._identifier)

    @classmethod
    def from_lenient(cls, maybe_gibberish):
        return cls(urls.url_fix(maybe_gibberish))

    @classmethod
    def from_template(cls, template, **kwargs):
        return URI(IRI(urls.url_unquote(uri_template(template, **kwargs))))
