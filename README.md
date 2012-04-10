# urilib

[![Build Status](https://secure.travis-ci.org/core/uricore.png?branch=master)](http://travis-ci.org/core/uricore)

**WARNING: Rough, raw, and fast changing code. Check back later. ;-)**

--

Example of use:

    >>> from httpcore.uri import URI
    >>> from httpcore.iri import IRI
    >>> iri = IRI(u'http://\N{SNOWMAN}/')
    >>> iri
    IRI(u'http://\u2603/')
    >>> uri = URI(iri)
    >>> uri
    URI('http://xn--n3h/')
    >>> iri.netloc
    u'http://\u2603/'
    >>> iri.hostname
    '\u2603'
    >>> iri.port is None
    True
    >>> iri.path
    u'/'
    >>> hasattr(iri, '__hash__')
    True
    >>> iri.replace(port=8000)
    IRI(u'http://\u2603:8000/')
    >>> iriq = iri.update_query({'foo': u'42'})
    >>> iriq
    IRI(u'http://\u2603/?foo=42')
    >>> iriq.update_query(foo=None)
    IRI(u'http://\u2603/')
    >>> iriq.query
    MultiDict([('foo', '42')])
    >>> URI.from_template('http://{domain}/find{?year*}', domain="example.com",
    ... year=("1965", "2000", "2012"))
    URI('http://example.com/find?year=1965&year=2000&year=2012')
