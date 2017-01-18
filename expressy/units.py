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

USE_PINT = bool(pint)


def make_ureg(*definitions):
    ureg = pint.UnitRegistry()
    map(ureg.define, definitions)
    return ureg


def parse(s):
    pass  # return ureg.parse_expression(s).to_base_units()


def insert_units(s, replacer):
    def match_is_pint(groups):
        return groups[2] and any(keyword.iskeyword(g.strip()) for g in groups)

    def function(match):
        return replacer(s) if match_is_pint(match) else s
