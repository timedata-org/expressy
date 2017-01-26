import unittest
import expressy
from expressy import expression, value


class ExpressyTest(unittest.TestCase):
    def test_units(self):
        self.assertEqual(expressy.parse('23 + 5')(), 28)

        with self.assertRaises(SyntaxError):
            expressy.parse('23Hz + 5Hz')
        v = expressy.parse_with_units('23Hz + 5Hz')()
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
