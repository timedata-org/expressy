import ast, operator


def Subscript(node):
    def get(getter, value):
        return getter(value)

    return get, [node.slice, node.value]


def Index(node):
    return operator.itemgetter, [node.value]


NONE = ast.NameConstant(value=None)


def Slice(node):
    def slicer(start, stop, step):
        s = slice(start, stop, step)
        return lambda x: x[s]

    return slicer, [node.lower or NONE, node.upper or NONE, node.step or NONE]
