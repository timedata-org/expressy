import builtins, math, unittest
from expressy import expression_maker, units, value


class ExpressyTest(unittest.TestCase):
    def assert_eval(self, s, symbols=None):
        self.assertEqual(expression_maker.make_expression(s)(), eval(s))

    def assert_eval_raises(self, exception, s):
        e = expression_maker.make_expression(s)
        with self.assertRaises(exception):
            e()

    def test_empty(self):
        with self.assertRaises(ValueError):
            expression_maker.make_expression('')

    def test_named_constant(self):
        self.assert_eval('True')
        self.assert_eval('False')
        self.assert_eval('None')

    def test_simple_literals(self):
        self.assert_eval('5')
        self.assert_eval('"False"')

    def test_collection(self):
        self.assert_eval('[1, 2, 3]')
        self.assert_eval('(1, 2, 3)')
        self.assert_eval('{1, 2, 3}')

    def test_dict(self):
        self.assert_eval('{}')
        self.assert_eval('{1: 2}')
        self.assert_eval('{1: 2, 2:{3: 4, 5: {}}}')

    def test_binary(self):
        self.assert_eval('1 + 2')
        self.assert_eval('1 / 2.3 * 9')
        self.assert_eval_raises(ZeroDivisionError, '1 / 0')

    def test_bool(self):
        self.assert_eval('True and "12"')
        self.assert_eval('False or "12" and 0 or []')

    def test_compare(self):
        self.assert_eval('1 < 2 < 3')
        self.assert_eval('1 > 2 < 1')
        self.assert_eval('1 != 3 >= 2 <= 1')

    def test_unary(self):
        self.assert_eval('not False')
        self.assert_eval('+(0 - 0)')
        self.assert_eval('-(0 - 1)')

    def test_if(self):
        self.assert_eval('False if 0 else "hello"')

    def test_subscript(self):
        self.assert_eval('"abcd"[1][0]')
        self.assert_eval_raises(IndexError, '"abcd"[10]')

    def test_call(self):
        self.assert_eval('max(-1, -2)')

    def test_importer_attribute(self):
        self.assert_eval('math.log(1)')

    def test_units(self):
        if units.pint:
            v = expression_maker.make_expression('23Hz + 5Hz')()
            self.assertEqual(v.units, '1 / second')
            self.assertEqual(v.magnitude, 28)
        pintless = expression_maker.make_expression_maker(use_pint=False)
        with self.assertRaises(SyntaxError):
            pintless('23Hz + 5Hz')

    def test_variable(self):
        bar = ['NO']

        def is_constant(name):
            return name != 'foo'

        def symbols(name):
            if name == 'foo':
                return lambda: bar[0]
            raise ValueError()

        e = expression_maker.make_expression_maker(is_constant, symbols)
        expression = e('foo()')
        self.assertFalse(expression.constant)
        self.assertEqual(expression(symbols), 'NO')
        bar[0] = 'YES'
        self.assertEqual(expression(symbols), 'YES')
