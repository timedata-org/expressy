"""A `Value` is a callable with a boolean property `constant`.
"""

class Constant(object):
    constant = True

    def __init__(self, value):
        self.evaluate = lambda: value


class Variable(object):
    constant = False

    def __init__(self, value):
        self.evaluate = value


def Value(function, *dependents):
    # Returns a Constant if all dependents are constant, otherwise a
    # Variable.
    constant = all(d.constant for d in dependents)
    return Constant(function()) if constant else Variable(function)


_VARIABLE_FUNCTIONS = set()


def is_variable_function(f):
    return _VARIABLE_FUNCTIONS.contains(f)


def variable_function(f):
    """A decorator to indicate that a function might return different
    values given the same arguments.
    """
    _VARIABLE_FUNCTIONS.add(f)
    return f
