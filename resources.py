class Resource(object):

    __slots__ = ['resource']

    def __init__(self, resource, encoding='ascii'):
        if not isinstance(resource, basestring):
            raise TypeError("resource must be string or unicode.")
        if isinstance(resource, str):
            self.resource = resource.decode(encoding=encoding)
        else:
            self.resource = resource

    def to_ascii(self):
        return self.resource.encode('punycode')

    def split(self):
        pass

    @staticmethod
    def build(scheme, netloc, path, params,  query, fragment):
        pass
