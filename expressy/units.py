from . import quotes
import keyword, functools, re


PINT_MATCH = r"""
    ( -? \d+ (?: \.\d* )? )          # A number with an optional decimal.
    ( \s* \w+ )                      # A unit.
    (?: ( \s* [ /] ) ( \s* \w+ ) )?  # A separator and a unit.
    (?: ( \s* [ /] ) ( \s* \w+ ) )?  # If I use * to repeat these, it only
    (?: ( \s* [ /] ) ( \s* \w+ ) )?  # captures the last one...
    (?: ( \s* [ /] ) ( \s* \w+ ) )?
    (?: ( \s* [ /] ) ( \s* \w+ ) )?
"""

PINT_MATCH_RE = re.compile(PINT_MATCH, re.VERBOSE)

try:
    import pint
except ImportError:
    pint = None


def make_unit_registry(definitions):
    ureg = pint.UnitRegistry()
    map(ureg.define, definitions)
    return ureg


def process_units(s, processor):
    def sub(match):
        groups = match.groups()
        has_keyword = any(keyword.iskeyword(g.strip()) for g in groups)
        has_units = groups[2] is not None
        can_process = has_units and not has_keyword

        body = match.groups(0)
        return processor(body) if can_process else body

    return quotes.process_unquoted(s, sub)


def make_injector(enable=True, definitions=None, injected_name='pint'):
    if enable and pint:
        def inject(symbols):
            unit_registry = make_unit_registry(definitions or [])

            def parse(s):
                return unit_registry.parse_expression(s).to_base_units()

            def wrap_name(s):
                return "%s('%s')" % (injected_name, s)

            def symbols_injected(name):
                return parse if name == injected_name else symbols(name)

            def preprocessor(s):
                return process_units(s, injected_name)

            return symbols_injected, preprocessor
    else:
        def inject(symbols):
            def preprocessor(s):
                return s

            return symbols, preprocessor

    return inject


injector = make_injector()
