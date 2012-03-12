class Resource(object):

    __slots__ = ['resource']

    def __init__(self, resource):
        self.resource = resource
        pass

    def to_ascii(self):
        pass

    def split(self):
        pass

    @staticmethod
    def build(scheme, netloc, path, params,  query, fragment):
        pass
