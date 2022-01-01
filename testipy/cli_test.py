import io
import unittest

from .cli import testipy
from .common_test import dedent


class TestCLI(unittest.TestCase):
    longMessage = False

    def test_cli_with_simple_test_file(self):
        out = io.StringIO()
        testipy("test_data/numbers_test.py", out)

        expected = dedent(
            """
            test_add PASS
            test_sub FAIL
                - expected 2 - 3 to be -1, got 5
            test_multiple_failures FAIL
                - failure message 1
                - failure message 2
            """
        )
        actual = out.getvalue()
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output:\n\n{expected}\ngot:\n\n{actual}",
        )
