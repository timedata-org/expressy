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
    def replace(match):
        groups = [(g or '').strip() for g in match.groups()]
        has_keyword = any(keyword.iskeyword(g) for g in groups)
        has_units = any(g.isalpha() for g in groups)
        can_process = has_units and not has_keyword

        s = match.group(0)
        return processor(s) if can_process else s

    def sub(s):
        return PINT_MATCH_RE.sub(replace, s)

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
                return process_units(s, wrap_name)

            return symbols_injected, preprocessor
    else:
        def inject(symbols):
            def preprocessor(s):
                return s

            return symbols, preprocessor

    return inject


injector = make_injector()
