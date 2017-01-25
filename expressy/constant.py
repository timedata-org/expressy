"""Rules for whether a function is constant - meaning that it always gives the
same result if called with the same values.

Most functions are constant.  Examples of non-constant functions are
time.time(), random.randint()...

A rule can return one of three values:

* False, meaning "the function is not constant".
* True, meaning "the function is constant"
* None, meaning "no information"
"""


def combine(*rules):
    def f(symbol):
        for r in rules:
            result = r(symbol)
            if result is not None:
                return result
    return f


def invert(*rules):
    def f(symbol):
        for r in rules:
            result = r(symbol)
            if result is not None:
                return not result
    return f


def prefix(name):
    def f(symbol):
        return symbol.startswith(name) or None
    return f


def top_level(symbol):
    return (symbol and ('.' not in symbol)) or None


CONSTANT = combine(
    top_level,
    invert(
        prefix('datetime.'),
        prefix('multiprocessing.'),
        prefix('threading.'),
        prefix('time.'),
        prefix('random.'),
    ),
)


def is_constant(symbol, default=None):
    constant = CONSTANT(symbol)
    return default if constant is None else constant
