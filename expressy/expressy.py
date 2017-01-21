import builtins

from . import expression, importer, units, value


def reduce_constant(expression, symbols, is_variable, is_late_binding):
    """Recursively evaluate every part of an expression that isn't a
    variable symbol or dependent on one.
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
    """Return False for any argument."""
    return False


def expressy(is_variable=accept_none, is_late_binding=accept_none,
             symbols=importer.importer, use_pint=False,
             pint_definitions=None, pint_registry=None, pint_name='pint',
             constant_reduction=True):
    """Returns an expression maker - a function that converts a string
    to a callable whose value is that expression

    Args:
       is_variable:  A function that returns True if a symbol is variable,
         otherwise False

       is_late_binding: A function that returns True if a symbol uses late
           binding - meaning that the value of the symbol is retrieved from
           scratch every time it is read.

        symbols: A symbol table that given a symbol either returns a symbol
            value, or throws a KeyError.

        use_pint: If True, try to use the pint unit conversion system.

        pint_definitions: a list of definitions to use if creating a new pint
            UnitRegistry.

        pint_registry: an existing pint registry to use

        pint_name: the replacement name to use in expressions to involve pint.
    """
    get_symbol, preprocessor = units.inject_pint(
        symbols, use_pint, pint_definitions, pint_name)

    def expression_maker(s):
        e = expression.parse_expression(preprocessor(s))
        if constant_reduction:
            return reduce_constant(e, get_symbol, is_variable, is_late_binding)

        return lambda: e(symbols)

    return expression_maker
