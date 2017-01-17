import keyword

QUOTE = "'"


def split_quoted(s):
    result = []
    for part in s.split(QUOTE):
        if result and result[-1].endswith('\\'):
            result[-1] = result[-1] + QUOTE + part
        else:
            result.append(part)

    if not len(result) % 2:
        raise ValueError('Unterminated quote.')

    return result


def process_unquoted(s, sub):
    def gen():
        *parts, last = split_quoted(s, QUOTE)
        for unquoted, quoted in zip([iter(parts)] * 2):
            yield sub(unquoted)
            yield QUOTE + quoted + QUOTE
        yield sub(last)

    return ''.join(gen())
