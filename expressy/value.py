"""A `Value` is a callable with a boolean property `constant`.
"""


class Value(object):
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


class Symbol(Value):
    def __call__(self):
        return self


_VARIABLES = set()


def is_variables(f):
    return _VARIABLES.contains(f)


def variable(f):
    """A decorator to indicate that a function might return different
    values given the same arguments.
    """
    _VARIABLES.add(f)
    return f
