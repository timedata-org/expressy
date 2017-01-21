from . import quotes
import keyword, re


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


def make_ureg(definitions):
    ureg = pint.UnitRegistry()
    map(ureg.define, definitions)
    return ureg


def parse(s):
    pass  # return ureg.parse_expression(s).to_base_units()


def insert_units(s, replacer):
    def sub(match):
        groups = match.groups()
        if any(keyword.iskeyword(g.strip()) for g in groups) or not groups[2]:
            return s
        return replacer(s)

    return quotes.process_unquoted(s, sub)


def inject_pint(symbols, use_pint, definitions, injected_name):
    if not (use_pint and pint):
        return symbols, lambda s: s

    # Find and replace all pint expressions in the string.
    parse = make_ureg(definitions or []).parse_expression

    def get_symbol(name):
        if name == injected_name:
            return lambda s: parse(s).to_base_units()
        return symbols(name)

    def preprocessor(s):
        return insert_units(s, lambda s: "%s('%s')" % (injected_name, s))

    return get_symbol, preprocessor
