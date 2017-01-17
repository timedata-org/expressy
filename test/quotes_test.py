import unittest
from expressy.quotes import split_quoted, process_unquoted


class SplitQuotedTest(unittest.TestCase):
    def test_trivial(self):
        self.assertEqual(split_quoted(""), [""])
        self.assertEqual(split_quoted("a"), ["a"])

    def test_splits(self):
        self.assertEqual(split_quoted("''"), ["", "", ""])
        self.assertEqual(split_quoted(
            r"I say, 'hello,' and I don\'t mean, 'hi'."),
            ["I say, ", "hello,", " and I don\\'t mean, ", "hi", "."])

    def test_failure(self):
        with self.assertRaises(ValueError):
            print(split_quoted(r"'"))
        split_quoted(r"\'")
        with self.assertRaises(ValueError):
            split_quoted(r"\''")
        split_quoted(r"''")
        with self.assertRaises(ValueError):
            split_quoted(r"a ' b")
        split_quoted(r"a \' b")
        with self.assertRaises(ValueError):
            split_quoted(r"a \' b '")
        split_quoted(r"a' b ' c")


class ProcessUnquotedTest(unittest.TestCase):
    def process(self, s):
        def sub(x):
            return x and ' '.join(['X', x, 'X'])

        return process_unquoted(s, sub)

    def test_trivial(self):
        self.assertEqual(self.process(""), "")

    def test_simple(self):
        self.assertEqual(self.process("hello"), "X hello X")

    def test_quotes(self):
        self.assertEqual(
            self.process(r"I say, 'hello,' and I don\'t mean, 'hi'."),
            "X I say,  X'hello,'X  and I don\\'t mean,  X'hi'X . X")
