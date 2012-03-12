# encoding: utf-8
from __future__ import unicode_literals


class _RI(object):
    def __init__(self, query_class=None):
        self.decoder


class IRI(_RI):

    def __init__(self, iri, charset='utf-8', query_class=None):
        super(IRI, self).__init__(query_class)
        if isinstance(iri, URI):
            iri = iri.to_iri()

    def to_uri(self):
        pass

class URI(_RI):

    def __init__(self, uri, query_class=None):
        super(IRI, self).__init__(query_class)
        if isinstance(uri, IRI):
            uri = uri.to_uri()

    def to_iri(self):
        pass
