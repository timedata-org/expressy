"""A `Value` is a callable with a boolean property `constant`.
"""


class Constant(object):
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


class Symbol(Constant):
    def __call__(self):
        return self


class Variable(object):
    # unused!
    def __init__(self, function, *args, **kwds):
        self.function = function
        self.args = args
        self.kwds = kwds

    def __call__(self):
        kwds = {k: v() for k, v in self.kwds.items()}
        return self.function(a() for a in self.args, **kwds)


_TEMPORALS = set()


def is_temporals(f):
    return _TEMPORALS.contains(f)


def temporal(f):
    """A decorator to indicate that a function might return different
    values given the same arguments.
    """
    _TEMPORALS.add(f)
    return f
