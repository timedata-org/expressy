import math, unittest

from expressy import importer


class ImporterTest(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            importer.importer('')

    def test_single(self):
        self.assertIs(importer.importer('math'), math)
        importer.importer('expressy')

    def test_failed_single(self):
        with self.assertRaises(ImportError):
            importer.importer('DOESNT_EXIST')

    def test_double(self):
        self.assertIs(importer.importer('math.log'), math.log)
        q = importer.importer('expressy.quotes')
        import expressy.quotes
        self.assertIs(q, expressy.quotes)

    def test_failed_double(self):
        with self.assertRaises(ImportError):
            importer.importer('math12.log')

        with self.assertRaises(ImportError):
            importer.importer('math.log12')

        with self.assertRaises(ImportError):
            importer.importer('expressy.log12')

    def test_longer(self):
        self.assertEqual(importer.importer('expressy.importer'), importer)
        self.assertEqual(importer.importer('expressy.importer.importer'),
                         importer.importer)

    def test_getter(self):
        self.assertIs(importer.importer.getter('math')(), math)
        self.assertIs(importer.importer.getter('math.log')(), math.log)
        with self.assertRaises(ImportError):
            importer.importer.getter('math.log12')
        untested_importer = importer.Importer(test_getter=False)
        getter = untested_importer.getter('math.log12')
        with self.assertRaises(ImportError):
            getter()
