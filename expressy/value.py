"""A `Value` returns a result when called."""


class Value(object):
    """Value returns a fixed value when called."""

    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


class Symbol(Value):
    """Symbol refers to a name in a symbol table."""

    def __call__(self):
        """Returns itself when evaluated so the result can't accidentally be
        used in futher calculations.
        """
        return self
