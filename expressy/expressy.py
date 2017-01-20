import builtins

from . import expression, importer, value


def evaluate_constants(expression, symbols, is_variable, is_late_binding):
    """Recursively evaluate every part that isn't a variable symbol or
    dependent on one.
    """

    def bind_dependents(executor, *dependents):
        expr = expression.Expression(executor, *dependents)
        return lambda: expr(symbols)

    def make_symbol(expr):
        assert not expr.dependents
        name = expr.executor.value
        variable = bind_dependents(expr.executor)

        if is_late_binding(name):
            return False, variable

        return is_variable(name), value.Value(variable())

    def make(expr):
        if isinstance(expr.executor, value.Symbol):
            return make_symbol(expr)

        constants, dependents = zip(*(make(d) for d in expr.dependents))
        variable = bind_dependents(expr.executor, *dependents)
        if all(constants):
            return True, value.Value(variable())
        return False, variable

    return make(expression)


def accept_none(_):
    return False


def expressy(s, is_variable=accept_none, is_late_binding=accept_none,
             symbols=importer.importer):
    expr = expression.parse_expression(s)
    return evaluate_constants(expr, symbols, is_variable, is_late_binding)
