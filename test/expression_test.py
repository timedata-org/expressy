import unittest
from expressy.expression import expression


class ExpressionTest(unittest.TestCase):
    def assertEval(self, s):
        self.assertEqual(expression(s)(), eval(s))

    def test_empty(self):
        with self.assertRaises(ValueError):
            expression('')

    def test_named_constant(self):
        self.assertEval('True')
        self.assertEval('False')
        self.assertEval('None')

    def test_simple_literals(self):
        self.assertEval('5')
        self.assertEval('"False"')

    def test_collection(self):
        self.assertEval('[1, 2, 3]')
        self.assertEval('(1, 2, 3)')
        self.assertEval('{1, 2, 3}')

    def test_dict(self):
        self.assertEval('{}')
        self.assertEval('{1: 2}')
        self.assertEval('{1: 2, 2:{3: 4, 5: {}}}')
