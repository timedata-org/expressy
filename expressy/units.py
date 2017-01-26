from . import expression, quotes
import keyword, functools, re

"""
This module is a hack to find Pint units in expressions and replace them
with a call to parse that string as a Pint expression.

See https://github.com/hgrecco/pint for more information about Pint.
"""
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
except ImportError:  # pragma: no cover
    pint = None


def process_units(s, processor):
    def replace(match):
        groups = [(g or '').strip() for g in match.groups()]
        has_keyword = any(keyword.iskeyword(g) for g in groups)
        has_units = any(g.isalpha() for g in groups)  # pragma: no cover
        can_process = has_units and not has_keyword

        s = match.group(0)
        return processor(s) if can_process else s

    def sub(s):
        return PINT_MATCH_RE.sub(replace, s)

    return quotes.process_unquoted(s, sub)


def inject(maker, definitions=None, injected_name='pint'):
    unit_registry = pint.UnitRegistry()
    for d in definitions or []:
        unit_registry.define(d)

    def parse(s):
        return unit_registry.parse_expression(s).to_base_units()

    def wrap_name(s):
        return "%s('%s')" % (injected_name, s)

    def symbols(name):
        return parse if name == injected_name else maker.symbols(name)

    new_maker = expression.Maker(maker.is_constant, symbols)

    def call(s):
        return new_maker(process_units(s, wrap_name))

    return call
