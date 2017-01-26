import unittest
from expressy import expression, make_expression, make_expression_units, value


class IntegrationTest(unittest.TestCase):
    def test_units(self):
        v = make_expression_units('23Hz + 5Hz')()
        self.assertEqual(v.units, '1 / second')
        self.assertEqual(v.magnitude, 28)

    def test_variable(self):
        bar = ['NO']

        def is_constant(name):
            return name != 'foo'

        def symbols(name):
            if name == 'foo':
                return lambda: bar[0]
            raise ValueError()

        maker = expression.Maker(is_constant, symbols)
        expr = maker('foo()')
        self.assertFalse(isinstance(expr, value.Value))
        self.assertEqual(expr(), 'NO')
        bar[0] = 'YES'
        self.assertEqual(expr(), 'YES')
