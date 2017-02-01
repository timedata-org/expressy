import datetime, json, math, unittest

from expressy.importer import importer


class ImporterTest(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            importer('')

    def test_single(self):
        self.assertIs(importer('math'), math)
        self.assertIs(importer('min'), min)
        importer('expressy')

    def test_failed_single(self):
        with self.assertRaises(ImportError):
            importer('DOESNT_EXIST')

    def test_double(self):
        self.assertIs(importer('math.log'), math.log)
        q = importer('expressy.quotes')
        import expressy.quotes
        self.assertIs(q, expressy.quotes)

    def test_failed_double(self):
        with self.assertRaises(ImportError):
            importer('math12.log')

        with self.assertRaises(ImportError):
            importer('math.log12')

        with self.assertRaises(ImportError):
            importer('expressy.log12')

    def test_self_import(self):
        self.assertEqual(importer('expressy.importer.importer'), importer)

    def test_self_import2(self):
        from expressy import importer
        self.assertEqual(importer.importer('expressy.importer'), importer)

    def test_make_object(self):
        td = importer.make(
            typename='datetime.timedelta',
            args=(5, 23),
            milliseconds=235,
        )
        self.assertEqual(td, datetime.timedelta(5, 23, milliseconds=235))

    def test_make_object_json(self):
        desc = """
        {
            "typename": "datetime.timedelta",
            "args": [5, 23],
            "milliseconds": 235
        }"""

        td = importer.make(**json.loads(desc))
        self.assertEqual(td, datetime.timedelta(5, 23, milliseconds=235))
