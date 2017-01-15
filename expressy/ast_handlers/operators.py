import ast, operator


"""This module provides a table mapping some AST node types to simple functions
implementing them."""


def operator_and(*values):
    for v in values:
        if not v:
            return v
    return v


def operator_or(*values):
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

    # Comparators
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


def operators(o):
    return OPERATORS[type(o)]
