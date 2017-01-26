import unittest
from expressy.constant import CONSTANT, CONSTANT_TRUE, prefix


class ConstantTest(unittest.TestCase):
    def test_prefix(self):
        pre = prefix('time.')
        self.assertTrue(pre('time.time'))
        self.assertIs(pre('foot.time'), None)

    def test_empty(self):
        self.assertTrue(CONSTANT_TRUE(''))
        self.assertIs(CONSTANT(''), None)

    def test_top_level(self):
        self.assertTrue(CONSTANT_TRUE('max'))
        self.assertTrue(CONSTANT('len'))

    def test_other(self):
        self.assertFalse(CONSTANT('time.time'))
        self.assertIs(CONSTANT('foo.bar'), None)
        self.assertTrue(CONSTANT('math.log'))
