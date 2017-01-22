import ast
from . import ast_handlers, value
from . value import Symbol, Value


class Expression(object):
    def __init__(self, executor, *dependents):
        self.executor = executor
        self.dependents = dependents

    def __call__(self, symbols):
        evaluated = [e(symbols) for e in self.dependents]
        v = self.executor(*evaluated)
        if isinstance(v, Symbol):
            return symbols(v.value)
        return v


def expression_from_node(node):
    executor, dependent_nodes = ast_handlers.handle(node)
    assert callable(executor), str(type(executor))

    # Recursive call here!
    dependents = (expression_from_node(n) for n in dependent_nodes)
    return Expression(executor, *dependents)


def parse_expression(s):
    module = ast.parse(s)
    if not module.body:
        raise ValueError('Empty expression')

    return expression_from_node(module.body[0])


def reduce_constant(expression, symbols, is_variable):
    """Recursively evaluate every part of an expression that isn't a
    variable symbol or dependent on one.
    """

    def make(expr):
        result = value.Value(expr(symbols))

        if isinstance(expr.executor, value.Symbol):
            return not is_variable(expr.executor.value), result

        if not expr.dependents:
            return True, result

        # Recursive call.
        constants, dependents = zip(*(make(d) for d in expr.dependents))
        if all(constants):
            return True, result

        reduced_expr = Expression(expr.executor, *dependents)
        return False, lambda: reduced_expr(symbols)

    return make(expression)
