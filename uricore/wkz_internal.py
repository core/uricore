class _Missing(object):

    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'

_missing = _Missing()


def _decode_unicode(value, charset, errors):
    """Like the regular decode function but this one raises an
    `HTTPUnicodeError` if errors is `strict`."""
    fallback = None
    if errors.startswith('fallback:'):
        fallback = errors[9:]
        errors = 'strict'
    try:
        return value.decode(charset, errors)
    except UnicodeError, e:
        if fallback is not None:
            return value.decode(fallback, 'replace')
        from werkzeug.exceptions import HTTPUnicodeError
        raise HTTPUnicodeError(str(e))
