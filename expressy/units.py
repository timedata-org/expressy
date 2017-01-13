try:
    import pint

    UREG = pint.UnitRegistry()
    UREG.define('beats=[]')
    UREG.define('bars=[beats]')

    def parse(s):
        return UREG.parse_expression(s).to_base_units()

except ImportError:
    def parse(s):
        return float(s)
