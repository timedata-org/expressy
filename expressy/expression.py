import ast
from . import ast_handlers, value

NO_SYMBOLS = {}.__getitem__


class Expression(object):
    def __init__(self, executor, *dependents):
        self.executor = executor
        self.dependents = dependents

    def __call__(self, symbols=NO_SYMBOLS):
        evaluated = [e(symbols) for e in self.dependents]
        v = self.executor(*evaluated)
        if isinstance(v, value.Symbol):
            return symbols(v.value)
        return v


def make_expression(node):
    executor, dependent_nodes = ast_handlers.handle(node)
    assert callable(executor), str(type(executor))

    # Recursive call to the constructor here!
    dependents = (make_expression(n) for n in dependent_nodes)
    return Expression(executor, *dependents)


def expression(s):
    module = ast.parse(s)
    if not module.body:
        raise ValueError('Empty expression')

    return make_expression(module.body[0])


def evaluate_constant(expression, is_variable, symbols=NO_SYMBOLS):
    """Recursively evaluate every part that isn't a variable symbol or
    dependent on one.
    """

    def make_constant(expr):
        if isinstance(expr.executor, value.Symbol):
            symbol_name = expr.executor.value
            if is_variable(symbol_name):
                return Expression(value.Value(result))

        else:
            dependents = [make_constant(d) for d in expr.dependents]
            if any(isinstance(d, Expression) for d in dependents):
                for i, d in dependents:
                    if not isinstance(d, Expression):
                        dependents[i] = Expression(value.Value(d))

                return Expression(expr.executor, *dependents)

        return expr(symbols)

    return make_constant(expression)
