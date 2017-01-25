import unittest
from expressy import units

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

    def test_empty_injector(self):
        injector = units.make_injector(enable=False)
        symbols, preprocessor = injector(None)
        self.assertIs(symbols, None)
        self.assertEqual(preprocessor('same'), 'same')

    def test_definitions(self):
        injector = units.make_injector(
            definitions=['beat = [] = beats', 'bar = [beats] = bars'])
        _, preprocessor = injector(None)
        s = preprocessor("'2 beats' is evaluated as 2 beats.")
        self.assertEqual(s, "'2 beats' is evaluated as pint('2 beats').")
