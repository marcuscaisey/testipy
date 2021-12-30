import io
import textwrap
import unittest

from cli import testipy


class TestCLI(unittest.TestCase):
    def test_cli_with_simple_test_file(self):
        out = io.StringIO()
        testipy("test_data/numbers_test.py", out)

        expected = dedent(
            """
            test_add PASS
            test_sub FAIL
                expected 2 - 3 to be -1, got 5
            """
        )
        actual = out.getvalue()
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output\n{expected}, got\n{actual}",
        )


def dedent(s: str) -> str:
    return textwrap.dedent(s).strip()
