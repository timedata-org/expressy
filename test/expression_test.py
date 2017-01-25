import builtins, math, fractions, unittest
from expressy.expression import parse_expression, reduce_constant
from expressy.importer import importer
from expressy import value

NO_SYMBOLS = {}.__getitem__


class ExpressionTest(unittest.TestCase):
    def assert_eval(self, s, symbols=None):
        self.assertEqual(parse_expression(s)(symbols), eval(s))

    def assert_eval_raises(self, exception, s):
        e = parse_expression(s)
        with self.assertRaises(exception):
            e(NO_SYMBOLS)

    def test_empty(self):
        with self.assertRaises(ValueError):
            parse_expression('')

    def test_named_constant(self):
        self.assert_eval('True')
        self.assert_eval('False')
        self.assert_eval('None')

    def test_simple_literals(self):
        self.assert_eval('5')
        self.assert_eval('"False"')
        self.assert_eval('b"012"')

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
        self.assert_eval('None is 2')
        self.assert_eval('None is not None')
        self.assert_eval('1 in [1, 2, 3]')
        self.assert_eval('1 not in [1, 2, 3]')

    def test_bool(self):
        self.assert_eval('True and "12"')
        self.assert_eval('False or "12" and 0 or []')
        self.assert_eval('False or "12"')

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
        self.assert_eval('"abcdefg"[2:3]')
        self.assert_eval('"abcdefg"[2:7:3]')
        self.assert_eval('"abcdefg"[2::3]')
        self.assert_eval('"abcdefg"[2:1]')
        self.assert_eval('"abcdefg"[2:1:-1]')

    def test_call(self):
        e = parse_expression('max(-1, -2)')
        with self.assertRaises(KeyError):
            e(NO_SYMBOLS)
        self.assertEqual(e(vars(builtins).get), -1)
        self.assert_eval('fractions.Fraction(1, denominator=2)', importer)
        self.assert_eval("'{foo}={bar}, {}'.format('hi', foo=1, bar=2)")

    def test_attribute(self):
        e = parse_expression('foo.bar.baz')
        with self.assertRaises(KeyError):
            e(NO_SYMBOLS)
        self.assertEqual(e({'foo.bar.baz': 23}.get), 23)

    def test_importer_attribute(self):
        self.assert_eval('math.log(1)', importer)

    def test_reduce_constant(self):
        e = parse_expression('1')
        f = reduce_constant(e, NO_SYMBOLS, lambda x: False)
        self.assertTrue(f.constant)
        self.assertEqual(f(NO_SYMBOLS), 1)

    def test_unimplemented(self):
        with self.assertRaises(ValueError):
            parse_expression('lambda x: x')

        with self.assertRaises(ValueError):
            parse_expression('...')

    def test_reduce_constant_variables(self):
        e = parse_expression('foo.bar() + foo.baz() + foo.bang')

        # We're going to set up a fake environment with these three variables,
        # mark foo.baz as variable, and then reduce constants... then
        # change all these and check that only foo.baz changed.

        bar, baz, bang = ['a'], ['b'], ['c']

        def symbols(name):
            if name == 'foo.bar':
                return lambda: bar[0]
            if name == 'foo.baz':
                return lambda: baz[0]
            if name == 'foo.bang':
                return bang[0]
            raise KeyError()

        def is_constant(name):
            return name != 'foo.baz'

        self.assertEqual(e(symbols), 'abc')

        f = reduce_constant(e, symbols, is_constant)
        self.assertFalse(f.constant)
        self.assertEqual(f(symbols), 'abc')
        bar[0], baz[0], bang[0] = 'xyz'
        self.assertEqual(f(symbols), 'ayc')
