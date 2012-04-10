# encoding: utf-8
from uricore import URI, IRI
from nose.tools import eq_ 
from uricore.template import uri_template

class CompatiblityOrderedDict(object):

    def __init__(self, items):
        self._items = items

    def iteritems(self):
        return iter(self._items)

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = CompatiblityOrderedDict


# http://tools.ietf.org/html/rfc6570#section-3.2
params = {
    'count': ("one", "two", "three"),
    'dom': ("example", "com"),
    'dub': "me/too",
    'hello': "Hello World!",
    'half': "50%",
    'var': "value",
    'who': "fred",
    'base': "http://example.com/home/",
    'path': "/foo/bar",
    'list': ("red", "green", "blue"),
    'year': ("1965", "2000", "2012"),
    'semi': ';',
    'v': 6,
    'x': 1024,
    'y': 768,
    'empty': "",
    'empty_keys': [],
    'undef': None,
    'list': ["red", "green", "blue"],
    #"keys": {'semi': ";", "dot": ".", "comma": ","},
    'keys': OrderedDict([('semi', ";"), ('dot', "."), ('comma', ",")]),
}

def check_template(template, expansion):
    eq_(uri_template(template, **params), expansion)


def test_composite_values():
    yield check_template, "find{?year*}", "find?year=1965&year=2000&year=2012"
    yield check_template, "www{.dom*}", "www.example.com"


def test_form_continuation_expansion():
    yield check_template, "{&who}", "&who=fred"
    yield check_template, "{&half}", "&half=50%25"
    yield check_template, "?fixed=yes{&x}", "?fixed=yes&x=1024"
    yield check_template, "{&x,y,empty}", "&x=1024&y=768&empty="
    yield check_template, "{&x,y,undef}", "&x=1024&y=768"
    yield check_template, "{&var:3}", "&var=val"
    yield check_template, "{&list}", "&list=red,green,blue"
    yield check_template, "{&list*}", "&list=red&list=green&list=blue"
    yield check_template, "{&keys}", "&keys=semi,%3B,dot,.,comma,%2C"
    yield check_template, "{&keys*}", "&semi=%3B&dot=.&comma=%2C"


def test_form_style_expansion():
    yield check_template, "{?who}", "?who=fred"
    yield check_template, "{?half}", "?half=50%25"
    yield check_template, "{?x,y}", "?x=1024&y=768"
    yield check_template, "{?x,y,empty}", "?x=1024&y=768&empty="
    yield check_template, "{?x,y,undef}", "?x=1024&y=768"
    yield check_template, "{?var:3}", "?var=val"
    yield check_template, "{?list}", "?list=red,green,blue"
    yield check_template, "{?list*}", "?list=red&list=green&list=blue"
    yield check_template, "{?keys}", "?keys=semi,%3B,dot,.,comma,%2C"
    yield check_template, "{?keys*}", "?semi=%3B&dot=.&comma=%2C"


def test_fragment_expansion():
    yield check_template, "{#var}", "#value"
    yield check_template, "{#hello}", "#Hello%20World!"
    yield check_template, "{#half}", "#50%25"
    yield check_template, "foo{#empty}", "foo#"
    yield check_template, "foo{#undef}", "foo"
    yield check_template, "{#x,hello,y}", "#1024,Hello%20World!,768"
    yield check_template, "{#path,x}/here", "#/foo/bar,1024/here"
    yield check_template, "{#path:6}/here", "#/foo/b/here"
    yield check_template, "{#list}", "#red,green,blue"
    yield check_template, "{#list*}", "#red,green,blue"
    yield check_template, "{#keys}", "#semi,;,dot,.,comma,,"
    yield check_template, "{#keys*}", "#semi=;,dot=.,comma=,"


def test_label_expansion():
    yield check_template, "{.who}", ".fred"
    yield check_template, "{.who,who}", ".fred.fred"
    yield check_template, "{.half,who}", ".50%25.fred"
    yield check_template, "www{.dom*}", "www.example.com"
    yield check_template, "X{.var}", "X.value"
    yield check_template, "X{.empty}", "X."
    yield check_template, "X{.undef}", "X"
    yield check_template, "X{.var:3}", "X.val"
    yield check_template, "X{.list}", "X.red,green,blue"
    yield check_template, "X{.list*}", "X.red.green.blue"
    yield check_template, "X{.keys}", "X.semi,%3B,dot,.,comma,%2C"
    yield check_template, "X{.keys*}", "X.semi=%3B.dot=..comma=%2C"
    yield check_template, "X{.empty_keys}", "X"
    yield check_template, "X{.empty_keys*}", "X"


def test_path_expansion():
    yield check_template, "{/who}", "/fred"
    yield check_template, "{/who,who}", "/fred/fred"
    yield check_template, "{/half,who}", "/50%25/fred"
    yield check_template, "{/who,dub}", "/fred/me%2Ftoo"
    yield check_template, "{/var}", "/value"
    yield check_template, "{/var,empty}", "/value/"
    yield check_template, "{/var,undef}", "/value"
    yield check_template, "{/var,x}/here", "/value/1024/here"
    yield check_template, "{/var:1,var}", "/v/value"
    yield check_template, "{/list}", "/red,green,blue"
    yield check_template, "{/list*}", "/red/green/blue"
    yield check_template, "{/list*,path:4}", "/red/green/blue/%2Ffoo"
    yield check_template, "{/keys}", "/semi,%3B,dot,.,comma,%2C"
    yield check_template, "{/keys*}", "/semi=%3B/dot=./comma=%2C"


def test_path_style_expansion():
    yield check_template, "{;who}", ";who=fred"
    yield check_template, "{;half}", ";half=50%25"
    yield check_template, "{;empty}", ";empty"
    yield check_template, "{;v,empty,who}", ";v=6;empty;who=fred"
    yield check_template, "{;v,bar,who}", ";v=6;who=fred"
    yield check_template, "{;x,y}", ";x=1024;y=768"
    yield check_template, "{;x,y,empty}", ";x=1024;y=768;empty"
    yield check_template, "{;x,y,undef}", ";x=1024;y=768"
    yield check_template, "{;hello:5}", ";hello=Hello"
    yield check_template, "{;list}", ";list=red,green,blue"
    yield check_template, "{;list*}", ";list=red;list=green;list=blue"
    yield check_template, "{;keys}", ";keys=semi,%3B,dot,.,comma,%2C"
    yield check_template, "{;keys*}", ";semi=%3B;dot=.;comma=%2C"


def test_reserved_expansion():
    yield check_template, "{+var}", "value"
    yield check_template, "{+hello}", "Hello%20World!"
    yield check_template, "{+half}", "50%25"
    yield check_template, "{base}index", "http%3A%2F%2Fexample.com%2Fhome%2Findex"
    yield check_template, "{+base}index", "http://example.com/home/index"
    yield check_template, "O{+empty}X", "OX"
    yield check_template, "O{+undef}X", "OX"
    yield check_template, "{+path}/here", "/foo/bar/here"
    yield check_template, "here?ref={+path}", "here?ref=/foo/bar"
    yield check_template, "up{+path}{var}/here", "up/foo/barvalue/here"
    yield check_template, "{+x,hello,y}", "1024,Hello%20World!,768"
    yield check_template, "{+path,x}/here", "/foo/bar,1024/here"
    yield check_template, "{+path:6}/here", "/foo/b/here"
    yield check_template, "{+list}", "red,green,blue"
    yield check_template, "{+list*}", "red,green,blue"
    yield check_template, "{+keys}", "semi,;,dot,.,comma,,"
    yield check_template, "{+keys*}", "semi=;,dot=.,comma=,"


def test_simple_string_expansion():
    yield check_template, "{var}", "value"
    yield check_template, "{hello}", "Hello%20World%21"
    yield check_template, "{half}", "50%25"
    yield check_template, "O{empty}X", "OX"
    yield check_template, "O{undef}X", "OX"
    yield check_template, "{x,y}", "1024,768"
    yield check_template, "{x,hello,y}", "1024,Hello%20World%21,768"
    yield check_template, "?{x,empty}", "?1024,"
    yield check_template, "?{x,undef}", "?1024"
    yield check_template, "?{undef,y}", "?768"
    yield check_template, "{var:3}", "val"
    yield check_template, "{var:30}", "value"
    yield check_template, "{list}", "red,green,blue"
    yield check_template, "{list*}", "red,green,blue"
    yield check_template, "{keys}", "semi,%3B,dot,.,comma,%2C"
    yield check_template, "{keys*}", "semi=%3B,dot=.,comma=%2C"


def test_test_prefix_values():
    yield check_template, "{var}", "value"
    yield check_template, "{var:20}", "value"
    yield check_template, "{var:3}", "val"
    yield check_template, "{semi}", "%3B"
    yield check_template, "{semi:2}", "%3B"


def test_variable_expansion():
    yield check_template, "{count}", "one,two,three"
    yield check_template, "{count*}", "one,two,three"
    yield check_template, "{/count}", "/one,two,three"
    yield check_template, "{/count*}", "/one/two/three"
    yield check_template, "{;count}", ";count=one,two,three"
    yield check_template, "{;count*}", ";count=one;count=two;count=three"
    yield check_template, "{?count}", "?count=one,two,three"
    yield check_template, "{?count*}", "?count=one&count=two&count=three"
    yield check_template, "{&count*}", "&count=one&count=two&count=three"


def test_uri_template():
    eq_(URI("http://example.com/value"),
        URI.from_template("http://example.com/{var}", var="value"))


def test_iri_template():
    eq_(IRI(u'http://\u2603/value'),
        IRI.from_template(u'http://\N{SNOWMAN}/{var}', var='value'))
