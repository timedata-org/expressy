import unittest
from expressy import expression, units

MATCH = units.PINT_MATCH_RE


class UnitsTest(unittest.TestCase):
    def test_trivial(self):
        self.assertTrue(not MATCH.match(''))
        self.assertTrue(not MATCH.match('2'))
        self.assertTrue(not MATCH.match('2.'))
        self.assertFalse(not MATCH.match('2.3'))  # Why?
        self.assertFalse(not MATCH.match('-2.3'))  # Why?

    def test_simple(self):
        self.assertEqual(MATCH.match('2Hz').group(1, 2), ('2', 'Hz'))
        self.assertEqual(MATCH.match('2 Hz').group(1, 2), ('2', ' Hz'))

    def processor(self, s):
        return "pint('%s')" % s

    def test_process_units(self):
        result = units.process_units(
            "'1Hz' is evaluated as 1Hz.", self.processor)
        self.assertEqual(result, "'1Hz' is evaluated as pint('1Hz').", )

    def test_definitions(self):
        maker = expression.Maker()
        injected = units.inject(
            maker, definitions=['beat = [] = beats', 'bar = [beats] = bars'])
        result = injected('2 beats')
        self.assertEqual(result().magnitude, 2)
