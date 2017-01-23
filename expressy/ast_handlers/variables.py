import ast, operator
from .. import value


def Name(node):
    return value.Symbol(node.id), []


def Attribute(node):  # a.b.c
    names = []
    n = node

    # Trace back the chain of attributes.
    while isinstance(n, ast.Attribute):
        names.append(n.attr)
        n = n.value

    if isinstance(n, ast.Name):
        # It's a top-level name.
        names.append(n.id)
        symbol = '.'.join(reversed(names))
        return value.Symbol(symbol), []

    # It's a relative name - so just use getattr.
    return operator.attrgetter(node.attr), [node.value]
