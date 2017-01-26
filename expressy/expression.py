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

    def resolve(self, symbols, is_constant):
        """Recursively evaluate every part of an expression that isn't a
        variable symbol or dependent on one.
        """

        result = self(symbols)

        if isinstance(self.executor, value.Symbol):
            if not is_constant(self.executor.value):
                return self

        elif self.dependents:
            # Recursive call.
            deps = [d.resolve(symbols, is_constant) for d in self.dependents]
            if not all(d.constant for d in deps):
                return Expression(self.executor, *deps)

        return Constant(result)


class Constant(Expression):
    constant = True

    def __init__(self, value):
        self.value = value

    def __call__(self, symbols):
        return self.value
