import ast
from . import literals, variables, expressions, subscripting

"""ast_handlers are functions which turn AST nodes into Values - recursively!

An ast_handler is a function which takes an AST node, and returns a pair:
   executor, [list of dependent AST nodes].

At execution time, the executor gets a list with one evaluated value for each
dependent AST node passed in."""


def _handlers():
    for module in literals, variables, expressions, subscripting:
        for name, function in module.__dict__.items():
            if name.startswith('_'):
                continue
            attr = getattr(ast, name, None)
            if attr:
                yield attr, function


HANDLERS = dict(_handlers())


def handle(node):
    try:
        return HANDLERS[type(node)](node)
    except:
        raise ValueError('Not yet implemented: %s' % type(node))
