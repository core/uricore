from uricore import URI
from nose.tools import assert_equals
from uricore.core import uri_template
from collections import OrderedDict

colors = ["red", "green", "blue"]
punc = OrderedDict([('semi', ";"), ('dot', "."), ('comma', ",")])


def eq_(a, b):
    assert_equals(a, b)


def test_simple_string_expansion():
    yield eq_, "value", uri_template("{var}", var="value")
    yield eq_, "Hello%20World%21", uri_template("{hello}", hello="Hello World!")


def test_reserved_string_expansion():
    yield eq_, "value", uri_template("{+var}", var="value")
    yield eq_, "Hello%20World!", uri_template("{+hello}", hello="Hello World!")
    yield eq_, "/foo/bar/here", uri_template("{+path}/here", path="/foo/bar")


def test_fragment_expansion():
    yield eq_, "X#value", uri_template("X{#var}", var="value")
    yield eq_, "X#Hello%20World!", uri_template("X{#hello}", hello="Hello World!")


def test_string_expansion_multiple_vars():
    yield eq_, "map?1024,768", uri_template("map?{x,y}", x=1024, y=768)
    yield eq_, "1024,Hello%20World%21,768", uri_template("{x,hello,y}", x=1024, y=768, hello="Hello World!")


def test_reserved_expansion_multiple_vars():
    yield eq_, "1024,Hello%20World!,768", uri_template("{+x,hello,y}", x=1024, y=768, hello="Hello World!")
    yield eq_, "/foo/bar,1024/here", uri_template("{+path,x}/here", path="/foo/bar", x=1024)


def test_fragment_expansion_muliple_vars():
    yield eq_, "#1024,Hello%20World!,768", uri_template("{#x,hello,y}", x=1024, y=768, hello="Hello World!")
    yield eq_, "#/foo/bar,1024/here", uri_template("{#path,x}/here", path="/foo/bar", x=1024)


def test_label_expansion_dot_prefix():
    yield eq_, "X.1024.768", uri_template("X{.x,y}", x=1024, y=768)
    yield eq_, "X.value", uri_template("X{.var}", var="value")


def test_path_segments_slash_prefix():
    yield eq_, "/value", uri_template("{/var}", var="value")
    yield eq_, "/value/1024/here", uri_template("{/var,x}/here", var="value", x=1024)


def test_path_stype_params_semicolon_prefix():
    yield eq_, ";x=1024;y=768", uri_template("{;x,y}", x=1024, y=768)
    yield eq_, ";x=1024;y=768;empty", uri_template("{;x,y,empty}", x=1024, y=768, empty=None)


def test_form_style_and_prefix():
    yield eq_, "?x=1024&y=768", uri_template("{?x,y}", x=1024, y=768)
    yield eq_, "?x=1024&y=768&empty", uri_template("{?x,y,empty}", x=1024, y=768, empty=None)


def test_form_style_continuation():
    yield eq_, "?fixed=yes&x=1024", uri_template("?fixed=yes{&x}", x=1024)
    yield eq_, "&x=1024&y=768&empty", uri_template("{&x,y,empty}", x=1024, y=768, empty=None)


def test_string_expansion_with_value_mods():
    yield eq_, "val", uri_template("{var:3}", var="value")
    yield eq_, "value", uri_template("{var:30}", var="value")
    yield eq_, "red,green,blue", uri_template("{list}", list=colors)
    yield eq_, "red,green,blue", uri_template("{list*}", list=colors)
    yield eq_, "semi,%3B,dot,.,comma,%2C", uri_template("{keys}", keys=punc)
    yield eq_, "semi=%3B,dot=.,comma=%2C", uri_template("{keys*}", keys=punc)


def test_reserved_expansion_with_value_mods():
    yield eq_, "/foo/b/here", uri_template("{+path:6}/here", path="/foo/bar")
    yield eq_, "red,green,blue", uri_template("{+list}", list=colors)
    yield eq_, "red,green,blue", uri_template("{+list*}", list=colors)
    yield eq_, "semi,;,dot,.,comma,,", uri_template("{+keys}", keys=punc)
    yield eq_, "semi=;,dot=.,comma=,", uri_template("{+keys*}", keys=punc)


def test_fragment_expansion_with_value_mods():
    yield eq_, "#/foo/b/here", uri_template("{#path:6}/here", path="/foo/bar")
    yield eq_, "#red,green,blue", uri_template("{#list}", list=colors)
    yield eq_, "#red,green,blue", uri_template("{#list*}", list=colors)
    yield eq_, "#semi,;,dot,.,comma,,", uri_template("{#keys}", keys=punc)
    yield eq_, "#semi=;,dot=.,comma=,", uri_template("{#keys*}", keys=punc)


def test_label_expansion_with_value_mods():
    yield eq_, "X.val", uri_template("X{.var:3}", var="value")
    yield eq_, "X.red,green,blue", uri_template("X{.list}", list=colors)
    yield eq_, "X.red.green.blue", uri_template("X{.list*}", list=colors)
    yield eq_, "X.semi,%3B,dot,.,comma,%2C", uri_template("X{.keys}", keys=punc)
    yield eq_, "X.semi=%3B.dot=..comma=%2C", uri_template("X{.keys*}", keys=punc)


def test_path_expansion_with_value_mods():
    yield eq_, "/v/value", uri_template("{/var:1,var}", var="value")
    yield eq_, "/red,green,blue", uri_template("{/list}", list=colors)
    yield eq_, "/red/green/blue", uri_template("{/list*}", list=colors)
    yield eq_, "/red/green/blue/%2Ffoo", uri_template("{/list*,path:4}",
                                                    list=colors, path="/foo/bar")
    yield eq_, "/semi,%3B,dot,.,comma,%2C", uri_template("{/keys}", keys=punc)
    yield eq_, "/semi=%3B/dot=./comma=%2C", uri_template("{/keys*}", keys=punc)


def test_path_style_expansion_with_value_mods():
    yield eq_, ";hello=Hello", uri_template("{;hello:5}", hello="Hello World!")
    yield eq_, ";list=red,green,blue", uri_template("{;list}", list=colors)
    yield eq_, ";list=red;list=green;list=blue", uri_template("{;list*}", list=colors)
    yield eq_, ";keys=semi,%3B,dot,.,comma,%2C", uri_template("{;keys}", keys=punc)
    yield eq_, ";semi=%3B;dot=.;comma=%2C", uri_template("{;keys*}", keys=punc)


def test_form_expansion_with_value_mods():
    yield eq_, "?var=val", uri_template("{?var:3}", var="value")
    yield eq_, "?list=red,green,blue", uri_template("{?list}", list=colors)
    yield eq_, "?list=red&list=green&list=blue", uri_template("{?list*}", list=colors)
    yield eq_, "?keys=semi,%3B,dot,.,comma,%2C", uri_template("{?keys}", keys=punc)
    yield eq_, "?semi=%3B&dot=.&comma=%2C", uri_template("{?keys*}", keys=punc)


def test_form_continuation_expansion_with_value_mods():
    yield eq_, "&var=val", uri_template("{&var:3}", var="value")
    yield eq_, "&list=red,green,blue", uri_template("{&list}", list=colors)
    yield eq_, "&list=red&list=green&list=blue", uri_template("{&list*}", list=colors)
    yield eq_, "&keys=semi,%3B,dot,.,comma,%2C", uri_template("{&keys}", keys=punc)
    yield eq_, "&semi=%3B&dot=.&comma=%2C", uri_template("{&keys*}", keys=punc)


def test_uri_template():
    assert_equals(URI("http://example.com/value"),
                  URI.from_template("http://example.com/{var}", var="value"))
