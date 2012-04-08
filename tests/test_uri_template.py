from nose.tools import eq_
from uricore.core import uri_template

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
    yield eq_, "/foo/bar,1024/here", uri_template("{+path,x}/here", path="/foo/bar")


def test_fragment_expansion_muliple_vars():
    yield eq_, "#1024,Hello%20World!,768", uri_template("{#x,hello,y}", x=1024, y=768, hello="Hello World!")
    yield eq_, "#/foo/bar,1024/here", uri_template("{#path,x}/here", path="/foo/bar")


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
    colors = ["red", "green", "blue"]
    punc = {'semi': ";", 'dot': ".", 'comma': ","}

    yield eq_, "val", uri_template("{var:3}", var="value")
    yield eq_, "value", uri_template("{var:30}", var="value")
    yield eq_, "red,green,blue", uri_template("{list}", list=colors)
    yield eq_, "red,green,blue", uri_template("{list*}", list=colors)
    yield eq_, "semi,%3B,dot,.,comma,%2C", uri_template("{keys}", keys=punc)
    yield eq_, "semi=%3B,dot=.,comma=%2C", uri_template("{keys*}", keys=punc)


def test_reserved_expansion_with_value_mods():
    colors = ["red", "green", "blue"]
    punc = {'semi': ";", 'dot': ".", 'comma': ","}

    yield eq_, "/foo/b/here", uri_template("{+path:6}/here}", path="/foo/bar")
    yield eq_, "red,green,blue", uri_template("{+list}", list=colors)
    yield eq_, "red,green,blue", uri_template("{+list*}", list=colors)
    yield eq_, "semi,;,dot,.,comma,,", uri_template("{+keys}", keys=punc)
    yield eq_, "semi=;,dot=.,comma=,", uri_template("{+keys*}", keys=punc)
