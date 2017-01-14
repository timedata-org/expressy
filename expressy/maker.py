import ast
from . import ast_handlers, value


class Maker(object):
    def __init__(self, importer):
        self.importer = importer

    def make_value(self, node):
        try:
            handler = ast_handlers.HANDLERS[type(node)]
        except:
            raise ValueError('Not yet implemented: %s' % type(node))
        return handler(node, self)

    def parse_value(self, s):
        """Parses a value.Value from a string."""
        module = ast.parse(s)
        if not module.body:
            return value.Constant(None)
        return self.make_value(module.body[0])
