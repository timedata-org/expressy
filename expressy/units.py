from . import quotes
import keyword, re

try:
    import pint
except ImportError:
    pint = None

USE_PINT = bool(pint)


PINT_MATCH = r"""
    ( -? \d+ (?: \.\d* )? )           # A number with an optional decimal.
    ( \s* \w+)                        # A unit.
    (?:  ( \s* [ /] ) ( \s* \w+ ) )?  # A separator and a unit.
    (?:  ( \s* [ /] ) ( \s* \w+ ) )?
    (?:  ( \s* [ /] ) ( \s* \w+ ) )?
    (?:  ( \s* [ /] ) ( \s* \w+ ) )?
    (?:  ( \s* [ /] ) ( \s* \w+ ) )?
"""
# The repetition is because otherwise you only get the last group from a match.

PINT_MATCH_RE = re.compile(PINT_MATCH, re.VERBOSE)


def make_unit_replacer(*definitions):
    if USE_PINT and pint:
        UREG = pint.UnitRegistry()
        # UREG.define('beats=[]')
        # UREG.define('bars=[beats]')


def insert_units(s, replacer):
    return s


    def parse(s):
        return UREG.parse_expression(s).to_base_units()



    def process_pint(s, replacer):
        def function(match):
            # Python identifiers take precedence.
            if any(keyword.iskeyword(g.strip() for g in match.groups())):
                return s
            return replacer(s)



except ImportError:
    def parse(s):
        return float(s)
