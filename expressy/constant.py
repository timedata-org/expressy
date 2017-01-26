"""Rules for whether a function is constant - meaning that it always gives the
same result if called with the same values.

Most functions are constant.  Examples of non-constant functions are
time.time(), random.randint()...

A rule can return one of three values:

* False, meaning "the function is not constant".
* True, meaning "the function is constant".
* None, meaning "no information".

Inverting the result of a rule switches False for True but leaves None alone.
"""


def combine(*rules):
    """Return a rule that combines all the other rules."""

    def rule(symbol):
        for r in rules:
            result = r(symbol)
            if result is not None:
                return result
    return rule


def invert(*rules):
    """Return a rule that combines all the other rules, inverted."""

    def rule(symbol):
        for r in rules:
            result = r(symbol)
            if result is not None:
                return not result
    return rule


def prefix(name):
    """Returns a rule that matches symbols that start with `name`."""
    def rule(symbol):
        return symbol.startswith(name) or None
    return rule


def top_level(symbol):
    """A rule that matches top-level symbols."""
    return (symbol and ('.' not in symbol)) or None


def true(symbol):
    """A rule that matches everything"""
    return True


CONSTANT = combine(
    top_level,
    prefix('copy.'),
    prefix('math.'),
    prefix('string.'),
    invert(
        prefix('datetime.'),
        prefix('multiprocessing.'),
        prefix('threading.'),
        prefix('time.'),
        prefix('random.'),
    ),
)

CONSTANT_TRUE = combine(CONSTANT, true)
