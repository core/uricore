from werkzeug import urls


class IRI(object):
    def __init__(self, iri, charset='utf-8'):
        pass

class URI(object):
    def __init__(self, uri, charset='ascii'):
        if isinstance(uri, IRI):
            uri = uri.to_uri()
