def Subscript(node, context):
    value = context.maker(node.value)
    slice = context.maker(node.slice)


def Index(node, context):
    return context.maker(node.value)
