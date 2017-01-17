# From BiblioPixel

import builtins, importlib


class Importer(object):
    def __init__(self, symbol_table=vars(builtins),
                 importer=importlib.import_module):
        """"""
        self.symbol_table = symbol_table
        self.importer = importer

    def __call__(self, symbol):
        try:
            return self.symbol_table[symbol]
        except KeyError:
            try:
                return self.importer(symbol)
            except ImportError:
                # Pop off the last segment, call recursively.
                *body, last = symbol.split('.')
                if not (body and last):
                    raise  # Can't recurse any more!

                parent = self('.'.join(body))
                _NONE = object()
                result = getattr(parent, last, _NONE)
                if result is _NONE:
                    raise
                return result


importer = Importer()
