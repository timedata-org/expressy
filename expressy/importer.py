# From BiblioPixel

import importlib


def import_symbol(symbol_path, builtins=vars(__builtins__),
                  import_module=import_lib.import_module):
    """Import a module or symbol_path within a module from its name."""
    try:
        return import_module(symbol_path)

    except ImportError:
        parts = symbol_path.split('.')
        part = parts.pop()
        if parts:
            # Call import_module recursively.
            namespace = import_symbol('.'.join(parts))
            return getattr(namespace, last_part)

        builtin = builtins.get(part, part)
        if builtin is part:
            raise

        return builtin
