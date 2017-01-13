import ast
from . import literals, variables, expressions, subscripting



        # Only handlers have an upper case first letter.
        self.handlers = {getattr(ast, k): v
                         for k, v in locals().items() if k[0].isupper()}


    def expression(self, node):
        try:
            handler = self.handlers[type(node)]
        except:
            raise ValueError('Not yet implemented: %s' % type(node))
        return handler(node)

    def parse(self, s):
        return context.maker(ast.parse(s))


BUILDER = ExpressionBuilder()
parse = BUILDER.parse
