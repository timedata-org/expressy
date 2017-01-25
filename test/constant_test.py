import unittest
from expressy import constant


NONE = object()
is_constant = constant.is_constant


class ConstantTest(unittest.TestCase):
    def test_prefix(self):
        pre = constant.prefix('time.')
        self.assertEqual(pre('time.time'), True)
        self.assertEqual(pre('foot.time'), None)

    def test_empty(self):
        self.assertEqual(is_constant('', NONE), NONE)

    def test_top_level(self):
        self.assertEqual(is_constant('max'), True)
        self.assertEqual(is_constant('len'), True)

    def test_other(self):
        self.assertEqual(is_constant('time.time'), False)
        self.assertEqual(is_constant('foo.bar', NONE), NONE)
