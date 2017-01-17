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
