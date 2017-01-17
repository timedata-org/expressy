from .. import value


def Num(node):
    return value.Constant(node.n), []


def Str(node):
    return value.Constant(node.s), []


def Bytes(node):
    return value.Constant(node.s), []


def NameConstant(node):
    return value.Constant(node.value), []


def List(node):
    return list, node.elts


def Tuple(node):
    return tuple, node.elts


def Set(node):
    return set, node.elts


def Dict(node):
    assert len(nodes.keys) == len(nodes.values)
    length = len(nodes.keys)

    def make_dict(*keys_values):
        keys, values = keys_values[:length], keys_values[length:]
        return {k: v for k, v in zip(keys, values)}

    return make_dict, list(nodes.keys) + list(nodes.values)


def Ellipsis(node):
    raise ValueError('Ellipsis (...) is not implemented.')


def NameConstant(node):
    return value.Constant(node.value), []
