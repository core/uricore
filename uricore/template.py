import re
from uricore.wkz_urls  import url_quote


def _format_mapping(operator, item):
    try:
        k, v, mapped = item
    except ValueError:
        k, v = item
        mapped = False

    if operator in ['#', '+']:
        # From http://tools.ietf.org/html/rfc6570#section-1.5
        safe = ':/?#[]@!$&\'\"()*/+,;='
    else:
        safe = ''

    if isinstance(v, (list, tuple)):
        v = ','.join(url_quote(x, safe=safe) for x in v)
    else:
        v = url_quote(v, safe=safe)

    if operator in [';', '?', '&'] or mapped:
        if not v:
            mid = '' if operator == ';' else '='
        else:
            mid = '='

        return u"{0}{1}{2}".format(url_quote(k, safe=safe), mid, v)
    else:
        return u"{0}".format(v)


def _template_joiner(operator):
    if operator in ['#', '+', '']:
        return ','
    elif operator == '?':
        return '&'
    elif operator == '.':
        return'.'
    return operator


def _varspec_expansion(operator, varspec, data):
    portion = None
    explode = False

    if ':' in varspec:
        varspec, portion = varspec.split(':', 1)
        portion = int(portion)

    if varspec.endswith('*'):
        varspec = varspec[:-1]
        explode = True

    value = data.get(varspec)

    if value == None:
        return []

    try:
        if len(value) == 0 and value != "":
            return []
    except TypeError:
        pass

    try:
        if explode:
            return [(k, v, True) for k,v in value.iteritems()]
        else:
            parts = []
            for k, v in value.iteritems():
                parts += [k, v]
            return [(varspec, parts)]
    except AttributeError:
        pass

    if isinstance(value, (list, tuple)):
        if explode:
            return [(varspec, v) for v in value]
        else:
            return [(varspec, value)]

    value = unicode(value)

    if portion is not None:
        value = value[:portion]

    return [(varspec, value)]


def uri_template(template, **kwargs):

    def template_expansion(matchobj):
        varlist = matchobj.group(1)
        operator = ''

        if re.match(r"\+|#|\.|/|;|\?|&", varlist):
            operator = varlist[0]
            varlist = varlist[1:]

        prefix = '' if operator == '+' else operator
        joiner = _template_joiner(operator)

        params = []
        for varspec in varlist.split(','):
            params += _varspec_expansion(operator, varspec, kwargs)

        uri = [_format_mapping(operator, item) for item in params]

        if not uri:
            return ""

        return prefix + joiner.join(uri)

    return re.sub(r"{(.*?)}", template_expansion, template)
