import operator
from .. import value


def Subscript(node):
    return (lambda s, v: s(v)), [node.slice, node.value]


def Index(node):
    return operator.itemgetter, [node.value]


def Slice(node):
    def slicer(start, stop, step):
        s = slice(start, stop, step)
        return lambda x: x[s]

    return slicer, [node.lower, node.upper, node.step]
