from . import value


def Num(node, context):
    return value.Value(node.n)


def Str(node, context):
    return value.Value(node.s)


def Bytes(node, context):
    return value.Value(node.s)


def NameConstant(node, context):
    return value.Value(node.value)


def collection(constructor):
    def f(node, context):
        values = [context.maker(e) for e in node.elts]

        def function():
            return constructor(v() for v in values)

        return value.Value(function, *values)

    return f


@collection
def List():
    return list


@collection
def Tuple():
    return tuple


@collection
def Set():
    return set


def Dict(node, context):
    # We always evaluate the keys immediately - we don't want them changing
    # underneath us!
    keys = [context.maker(k)() for k in node.keys]
    values = [context.maker(k) for k in node.values]

    def function():
        return {k: v() for k, v in zip(keys, values)}

    return value.Value(function, *values)


def Ellipsis(node, context):
    raise ValueError('Ellipsis (...) is not implemented.')


def NameConstant(node, context):
    return value.Value(node.value)
