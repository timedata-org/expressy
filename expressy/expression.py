import ast
from . import ast_handlers, value


class Expression(object):
    constant = False

    def __init__(self, executor, *dependents):
        self.executor = executor
        self.dependents = dependents

    def __call__(self, symbols):
        evaluated = [e(symbols) for e in self.dependents]
        v = self.executor(*evaluated)
        if isinstance(v, value.Symbol):
            return symbols(v.value)
        return v


class Constant(object):
    constant = True

    def __init__(self, value):
        self.value = value

    def __call__(self, symbols):
        return self.value


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
        result = expr(symbols)

        if isinstance(expr.executor, value.Symbol):
            if is_variable(expr.executor.value):
                return expr

        elif expr.dependents:
            # Recursive call.
            dependents = [make(d) for d in expr.dependents]
            if not all(d.constant for d in dependents):
                return Expression(expr.executor, *dependents)

        return Constant(result)

    return make(expression)
