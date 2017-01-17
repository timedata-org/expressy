import unittest

from expressy import importer

import_symbol = importer.importer


class ImporterTest(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            import_symbol('')

    def test_single(self):
        import_symbol('math')
        import_symbol('expressy')

    def test_failed_single(self):
        with self.assertRaises(ImportError):
            import_symbol('DOESNT_EXIST')

    def test_double(self):
        import_symbol('math.log')
        import_symbol('expressy.quotes')

    def test_failed_double(self):
        with self.assertRaises(ImportError):
            import_symbol('math12.log')

        with self.assertRaises(ImportError):
            import_symbol('math.log12')

        with self.assertRaises(ImportError):
            import_symbol('expressy.log12')

    def test_longer(self):
        self.assertEqual(import_symbol('expressy.importer'), importer)
        self.assertEqual(import_symbol('expressy.importer.importer'),
                         import_symbol)
