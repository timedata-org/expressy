import ast, functools, operator
from .. import value


def Expr(node, context):
    return context.make_value(node.value)


def operator_and(values):
    for v in values:
        if not v:
            return v
    return v


def operator_or(values):
    for v in values:
        if v:
            return v
    return v


OPERATORS = {
    # UnaryOp.
    ast.Invert: operator.invert,
    ast.Not: operator.not_,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,

    # BinOp
    ast.Add: operator.add,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Mult: operator.mul,
    ast.Pow: operator.pow,

    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.BitAnd: operator.and_,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
    # ast.MatMult: can't do that yet.

    # BoolOp
    ast.And: operator_and,
    ast.Or: operator_or,
}


# Decorate a handler that wraps a standard operator.
def operator(f):
    def handler(node, context):
        args = [context.make_value(d) for d in f(node)]
        operator = OPERATORS[node.op]

        def function():
            return operator(*(d() for d in args))

        return value.Value(function, *args)
    return handler


@operator
def BinOp(node):  # a + b
    return node.left, node.right


@operator
def BoolOp(node):  # x and y and z
    return node.values


@operator
def UnaryOp(node):  # -a, not a, +a, ~a
    return node.operand,
import operator


COMPARATORS = {
    ast.Eq: operator.eq,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.NotEq: operator.ne,
    ast.Is: (lambda x, y: x is y),
    ast.IsNot: (lambda x, y: x is not y),
    ast.In: (lambda x, y: x in y),
    ast.NotIn: (lambda x, y: x not in y),
}


def Compare(node, context):  # 1 < 2 < 4 > 5
    left = context.make_value(node.left)
    ops = [COMPARATORS[o] for o in node.ops]
    values = [context.make_value(c) for c in node.comparators]
    op_values = zip(ops, values)

    def function():
        previous = left()
        for op, value in op_values:
            value = value()
            if not op(previous, value):
                return False
            previous = value
        return True

    return value.Value(function, left, *values)


def Call(node, context):  # f(a, *b, **c)
    arg = [context.make_value(a) for a in node.arg]
    kwds = {k.arg: context.make_value(k.value) for k in node.keywords}

    function = context.make_value(node.func)
    assert isinstance(node.func, (ast.Attribute, ast.Name))
    assert function.constant

    f = functools.partial(function(), *arg, **kwds)
    return value.Value(f, *(arg + list(kwds.values())))


def IfExp(node, context):  # x if y else z
    body = context.make_value(node.body)
    test = context.make_value(node.test)
    orelse = context.make_value(node.orelse)

    def function():
        return body() if test() else orelse()

    return value.Value(function, body, test, orelse)
