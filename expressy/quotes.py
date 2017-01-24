QUOTE = "'"


def split_quoted(s):
    """Split a string with quotes, some possibly escaped, into a list of
    alternating quoted and unquoted segments.  Raises a ValueError if there are
    unmatched quotes.

    Both the first and last entry are unquoted, but might be empty, and
    therefore the length of the resulting list must be an odd number.
    """
    result = []
    for part in s.split(QUOTE):
        if result and result[-1].endswith('\\'):
            result[-1] = result[-1] + QUOTE + part
        else:
            result.append(part)

    if not len(result) % 2:
        raise ValueError('Unmatched quote.')

    return result


def process_unquoted(s, sub):
    """Splits a string into unquoted and quoted segments, applies a substitution
    function to the unquoted segments only, and joins it back together again.
    """
    def gen():
        *parts, last = split_quoted(s)
        for unquoted, quoted in zip(*([iter(parts)] * 2)):
            yield sub(unquoted)
            yield QUOTE + quoted + QUOTE
        yield sub(last)

    return ''.join(gen())
