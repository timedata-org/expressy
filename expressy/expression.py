import ast
from . import ast_handlers, value

NO_SYMBOLS = {}.__getitem__


class Expression(object):
    def __init__(self, executor, dependent_expressions):
        self.executor = executor
        self.dependent_expressions = dependent_expressions

    def __call__(self, symbols=NO_SYMBOLS):
        evaluated = [e(symbols) for e in self.dependent_expressions]
        v = self.executor(*evaluated)
        return symbols(v.value) if isinstance(v, value.Symbol) else v


def make_expression(node):
    executor, dependent_nodes = ast_handlers.handle(node)
    assert callable(executor), str(type(executor))

    # Recursive call to the constructor here!
    dependent_expressions = (make_expression(n) for n in dependent_nodes)

    return Expression(executor, tuple(dependent_expressions))


def expression(s):
    module = ast.parse(s)
    if not module.body:
        raise ValueError('Empty expression')

    return make_expression(module.body[0])


def evaluate_constant(expression, symbols, variables):
    """Evaluate every part that isn't a variable symbol or dependent on it."""
    pass
