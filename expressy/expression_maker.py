import builtins
from . import expression, importer, units, value


def make_expression_maker(
        is_variable=None, symbols=importer.importer, use_pint=True):
    """Returns an expression maker - a function that converts a string
    to a callable whose value is that expression

    Args:
       is_variable:  A function that returns True if a symbol is variable,
         otherwise False

        symbols: A symbol table that given a symbol either returns a symbol
            value, or throws a KeyError.

        unit_injector: injects unit definitions into the expression
            string and into the
    """
    injector = units.injector if use_pint else units.empty_injector
    symbols, preprocessor = injector(symbols)

    def make_expression(s):
        e = expression.parse_expression(preprocessor(s))
        if is_variable:
            return expression.reduce_constant(e, symbols, is_variable)

        return lambda: e(symbols)

    return make_expression


make_expression = make_expression_maker()