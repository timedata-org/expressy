import ast
from . import ast_handlers, value


class Expression(object):
    def __init__(self, node):
        self.executor, dependents = ast_handlers.handle(node)
        assert callable(self.executor), str(type(self.executor))

        # Recursive call to the constructor here!
        self.dependent_expressions = tuple(Expression(d) for d in dependents)

    def __call__(self, symbols=None):
        symbols = symbols or {}
        evaluated = (d(symbols) for d in self.dependent_expressions)
        v = self.executor(*evaluated)
        return symbols(v.value) if isinstance(v, value.Symbol) else v


def expression(s):
    module = ast.parse(s)
    if not module.body:
        raise ValueError('Empty expression')

    return Expression(module.body[0])
