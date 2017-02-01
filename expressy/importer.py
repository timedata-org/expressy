import builtins, importlib


class Importer(object):
    """An Importer imports either a namespace or a symbol within a namespace.

    It's like a more general version of importlib.import_module which handles
    builtins and attributes within a module.

    An Importer has a symbol_table that's always used to try to resolve
    symbols before anything else.  By default, symbol_table is the Python
    built-in symbols as found in the module `builtins`:

        ArithmeticError, AssertionError, ..., abs, all, ... zip

    It also has a module_importer which imports Python modules or raises
    an ImportError.  By default this is just importlib.import_module.
    """

    def __init__(self, symbol_table=vars(builtins),
                 module_importer=importlib.import_module):
        """Args:
            symbol_table: a dictionary which maps symbols to values.
            module_importer: a function that imports namespaces by path or
                raises an ImportError otherwise.
            """
        self.symbol_table = symbol_table
        self.module_importer = module_importer

    def getter(self, symbol):
        """Return a function that gets the value for symbol when called.

        This function will return the new value when that value changes,
        but will *not* reload a module when that module changes.
        """
        try:
            value = self.symbol_table[symbol]
            return lambda: value
        except KeyError:
            pass

        *body, last = symbol.split('.')
        try:
            imported = self.module_importer(symbol)
            return lambda: imported
        except ImportError:
            if not (body and last):
                raise  # Can't recurse any more!

        # Call getter recursively on the parent.
        parent_name = '.'.join(body)
        parent = self.getter(parent_name)
        parent_value = parent()

        def getter():
            try:
                return getattr(parent_value, last)
            except AttributeError:
                raise ImportError("No module named '%s'" % symbol, name=symbol)

        return getter

    def __call__(self, symbol):
        """Import the value for symbol, or raise an ImportError if it can't be
        found.
        """
        return self.getter(symbol)()

    def make(self, typename, args=(), **kwds):
        """Make an object from its type.

        Args:
            typename: name of the class or other constructor for the object.
            args: positional arguments to the constructor.
            keyword arguments to the constructor.
        """
        constructor = self(typename)
        return constructor(*args, **kwds)


importer = Importer()
