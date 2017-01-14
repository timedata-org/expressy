from . import literals, variables, expressions, subscripting

"""ast_handlers are functions which turn AST nodes into Values - recursively!

An ast_handler is a function which takes an AST node and a Context, and returns
a Value.
"""


def _handlers():
    for module in literals, variables, expressions, subscripting:
        for name, function in module.__dict__.items():
            attr = getattr(ast, name, None)
            if attr:
                yield attr, function


HANDLERS = dict(_handlers())
