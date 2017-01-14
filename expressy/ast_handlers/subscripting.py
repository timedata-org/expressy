def Subscript(node, context):
    value = context.make_value(node.value)
    slice = context.make_value(node.slice)


def Index(node, context):
    return context.make_value(node.value)
