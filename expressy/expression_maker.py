import builtins
from . import expression, importer, units, value


def make_expression_maker(
        is_constant=None, symbols=importer.importer, use_pint=True):
    """Returns an expression maker - a function that converts a string
    to a callable whose value is that expression

    Args:
       is_constant:  A function that returns True if a symbol refers to a
           function that always returns the same value when given the same
           arguments.

        symbols: A symbol table that given a symbol either returns a symbol
            value, or throws a KeyError.

        unit_injector: injects unit definitions into the expression
            string and into the
    """
    injector = units.injector if use_pint else units.empty_injector
    symbols, preprocessor = injector(symbols)

    def make_expression(s):
        e = expression.Expression.parse(preprocessor(s))
        if is_constant:
            return e.resolve(symbols, is_constant)

        return lambda: e(symbols)

    return make_expression


make_expression = make_expression_maker()
