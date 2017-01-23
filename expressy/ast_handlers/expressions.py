from . operators import operators


def Expr(node):  # A container for an expression.
    return (lambda x: x), [node.value]


def BinOp(node):  # a + b
    return operators(node.op), [node.left, node.right]


def BoolOp(node):  # a and b and c
    return operators(node.op), node.values


def UnaryOp(node):  # -a, not a, +a, ~a
    return operators(node.op), [node.operand]


def Compare(node):  # a < b < c > d
    ops = [operators(o) for o in node.ops]

    def compare(left, *values):
        assert len(ops) == len(values)
        for op, value in zip(ops, values):
            if not op(left, value):
                return False
            left = value
        return True

    return compare, [node.left] + node.comparators


def Call(node):  # f(a, *b, **c)
    if not node.keywords:
        def call(caller, *args):
            return caller(*args)

        return call, [node.func] + node.args

    arg_length = len(node.args)
    kv = [(k.arg, k.value) for k in node.keywords]
    keys, value_nodes = zip(*kv)

    def call(caller, *args_values):
        args, values = args_values[:arg_length], args_values[arg_length:]
        return caller(*args, **dict(zip(keys, values)))

    return call, [node.func] + node.args + list(value_nodes)


def IfExp(node):  # a if b else c
    def if_exp(body, test, orelse):
        return body if test else orelse

    return if_exp, [node.body, node.test, node.orelse]
