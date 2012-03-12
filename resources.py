# encoding: utf-8
from __future__ import unicode_literals


class IRI(object):

    def __init__(self, iri, charset='utf-8'):
        pass

    def to_uri(self):
        pass


class URI(object):

    def __init__(self, uri, charset='ascii'):
        if isinstance(uri, IRI):
            uri = uri.to_uri()
