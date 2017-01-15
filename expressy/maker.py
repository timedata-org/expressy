import ast
from . import ast_handlers, value


class Expression(object):
    def __init__(self, node)
        self.executor, dependents = ast_handlers.handle(node)

        # Recursive call to the constructor here!
        self.dependents = tuple(Expression(d) for d in dependents)

    def __call__(self, symbols=None):
        v = self.executor(*(d() for d in self.descendents()))
        if isinstance(v, value.Symbol):
            v = symbols(v.value)
        return v


def expression(s):
    module = ast.parse(s)
    if not module.body:
        raise ValueError('Empty expression')

    return Expression(module.body[0])
