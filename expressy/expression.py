import ast
from . import ast_handlers, constant, importer, value


class Expression(object):
    def __init__(self, executor, *dependents):
        self.executor = executor
        self.dependents = dependents

    def __call__(self, symbols):
        evaluated = [e(symbols) for e in self.dependents]
        v = self.executor(*evaluated)
        if isinstance(v, value.Symbol):
            return symbols(v.value)
        return v

    @staticmethod
    def from_node(node):
        executor, dependent_nodes = ast_handlers.handle(node)
        assert callable(executor), str(type(executor))

        # Recursive call here!
        dependents = (Expression.from_node(n) for n in dependent_nodes)
        return Expression(executor, *dependents)

    @staticmethod
    def parse(s):
        module = ast.parse(s)
        if not module.body:
            raise ValueError('Empty expression')

        return Expression.from_node(module.body[0])

    def resolve(self, symbol_table, is_constant):
        """Recursively evaluate every part of an expression that isn't a
        variable symbol or dependent on one.
        """
        def resolver(expr):
            if isinstance(expr.executor, value.Symbol):
                if is_constant and not is_constant(expr.executor.value):
                    return expr, False

            elif expr.dependents:
                recursion = [resolver(d) for d in expr.dependents]
                dependents, constants = zip(*recursion)
                if not all(constants):
                    return Expression(expr.executor, *dependents), False

            result = expr(symbol_table)
            return Expression(value.Value(result)), True

        expr, constant = resolver(self)
        return expr.executor if constant else Bound(expr, symbol_table)


class Bound(object):
    """Binds an expression to a symbol_table."""

    def __init__(self, expression, symbol_table):
        self.expression = expression
        self.symbol_table = symbol_table

    def __call__(self):
        """Returns the expression called on the symbol table."""
        return self.expression(self.symbol_table)


class Maker(object):
    """Parses expressions into callables."""

    def __init__(self, is_constant=constant.CONSTANT,
                 symbols=importer.importer):
        """
        Args:
            is_constant:  a function that returns True if a symbol is a
                constant function, False if it is not, and None if unknown.

            symbols: a function that returns the resolution of a symbol, or
                raises an ImportError.
        """
        self.is_constant = is_constant
        self.symbols = symbols

    def __call__(self, s):
        """Parse a string representing an expression and return a callable
        which when called returns the value of the expression.

        If the expression is constant, returns a value.Value, otherwise
        an expression.Bound.
        """
        expr = Expression.parse(s)
        return expr.resolve(self.symbols, self.is_constant)
