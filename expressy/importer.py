# From BiblioPixel

import builtins, importlib


class Importer(object):
    def __init__(self, symbol_table=vars(builtins),
                 importer=importlib.import_module,
                 test_getter=True):
        self.symbol_table = symbol_table
        self.importer = importer
        self.test_getter = test_getter

    def getter(self, symbol):
        try:
            value = self.symbol_table[symbol]
            return lambda: value
        except KeyError:
            pass

        *body, last = symbol.split('.')
        try:
            imported = self.importer(symbol)
            return lambda: imported
        except ImportError:
            if not (body and last):
                raise  # Can't recurse any more!

        # Call recursively.
        parent_name = '.'.join(body)
        parent = self.getter(parent_name)
        parent_value = parent()

        def getter():
            try:
                return getattr(parent_value, last)
            except AttributeError:
                raise ImportError("No module named '%s'" % symbol, name=symbol)

        self.test_getter and getter()
        return getter

    def __call__(self, symbol):
        return self.getter(symbol)()


importer = Importer()
