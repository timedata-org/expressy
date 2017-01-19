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


def expression(s):
    module = ast.parse(s)
    if not module.body:
        raise ValueError('Empty expression')

    return expression_from_node(module.body[0])


def evaluate_constant(expression, is_variable, is_late_binding, symbols):
    """Recursively evaluate every part that isn't a variable symbol or
    dependent on one.
    """

    def bind_dependents(executor, *dependents):
        expression = Expression(executor, *dependents)
        return lambda: expression(symbols)

    def make_symbol(expr):
        assert not expr.dependents
        name = expr.executor.value
        variable = bind_dependents(expr.executor)

        if is_late_binding(name):
            return False, variable

        return is_variable(name), Value(variable())

    def make(expr):
        if isinstance(expr.executor, Symbol):
            return make_symbol(expr)

        constants, dependents = zip(*(make(d) for d in expr.dependents))
        variable = bind_dependents(expr.executor, *dependents)
        if all(constants):
            return True, Value(variable())
        return False, variable

    return make(expression)
