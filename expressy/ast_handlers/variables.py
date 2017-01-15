from . import value


def Name(node):
    return value.Symbol(node.id), []


def Attribute(node):  # a.b.c
    names = []
    while isinstance(node, ast.Attribute):
        names.append(node.attr)
        node = node.value
    assert isinstance(node, ast.Name)
    names.append(node.id)
    symbol = '.'.join(reversed(names))
    return value.Symbol(symbol), []
