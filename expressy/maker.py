import ast
from . import importer, literals, value, variables, expressions, subscripting


class Context(object):
    def __init__(self, symbol_table=importer.import_symbol):
        self.symbol_table = symbol_table

        def ast_handlers():
            for ns in HANDLER_NAMESPACES:
                for name, function in ns.__dict__.items():
                    attr = getattr(ast, name, None)
                    if attr:
                        yield attr, function

        self.handlers = dict(ast_handlers())

    def maker(self, node):
        try:
            handler = self.handlers[type(node)]
        except:
            raise ValueError('Not yet implemented: %s' % type(node))
        return handler(node)

    def parse(self, s):
        module = ast.parse(s)
        if not module.body:
            return value.Constant(None)
        return self.maker(module.body[0])


HANDLER_NAMESPACES = literals, variables, expressions, subscripting
CONTEXT = Context()
parse = CONTEXT.parse
