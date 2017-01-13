from . import value


def Name(node, context):
    return value.Value(symbol_table(node.id))


def Attribute(node, context):  # a.b.c
    names = []
    while isinstance(node, ast.Attribute):
        names.append(node.attr)
        node = node.value
    assert isinstance(node, ast.Name)
    names.append(node.id)
    symbol = '.'.join(reversed(names))
    return value.Value(context.symbol_table(symbol))
