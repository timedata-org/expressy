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
