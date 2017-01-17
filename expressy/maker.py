import ast
from . import ast_handlers, value


class Expression(object):
    def __init__(self, node)
        self.executor, dependents = ast_handlers.handle(node)

        # Recursive call to the constructor here!
        self.dependent_expressions = tuple(Expression(d) for d in dependents)

    def __call__(self, symbols):
        evaluated = (d(symbols) for d in self.dependent_expressions)
        v = self.executor(*evaluated)
        return symbols(v.value) isinstance(v, value.Symbol) else f


def expression(s):
    module = ast.parse(s)
    if not module.body:
        raise ValueError('Empty expression')

    return Expression(module.body[0])
