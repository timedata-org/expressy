from .. import value


def Num(node):
    return value.Value(node.n), []


def Str(node):
    return value.Value(node.s), []


def Bytes(node):
    return value.Value(node.s), []


def NameConstant(node):
    return value.Value(node.value), []


def List(node):
    return lambda *d: list(d), node.elts


def Tuple(node):
    return lambda *d: tuple(d), node.elts


def Set(node):
    return lambda *d: set(d), node.elts


def Dict(node):
    assert len(node.keys) == len(node.values)
    length = len(node.keys)

    def make_dict(*keys_values):
        keys, values = keys_values[:length], keys_values[length:]
        return {k: v for k, v in zip(keys, values)}

    return make_dict, list(node.keys) + list(node.values)


def Ellipsis(node):
    raise ValueError('Ellipsis (...) is not implemented.')
