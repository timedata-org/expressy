import unittest
from expressy.expression import expression

class ExpressionTest(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            expression('')

    def test_named_constant(self):
        self.assertEqual(expression('True')(), True)
        self.assertEqual(expression('False')(), False)
        self.assertEqual(expression('None')(), None)

    def test_simple_literals(self):
        self.assertEqual(expression('5')(), 5)
        self.assertEqual(expression('"False"')(), 'False')

    def test_collection(self):
        self.assertEqual(expression('[1, 2, 3]')(), [1, 2, 3])
        self.assertEqual(expression('(1, 2, 3)')(), (1, 2, 3))
        self.assertEqual(expression('{1, 2, 3}')(), {1, 2, 3})
