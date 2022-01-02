import io
import unittest

from .cli import testipy
from .common_test import dedent, get_project_root


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
                - failure message
                - multiple failures are allowed in the same test
            test_exceptions_error_the_test ERROR
                Traceback (most recent call last):
                  File "{project_root}/test_data/numbers_test.py", line 33, in test_exceptions_error_the_test
                    raises_exception()
                  File "{project_root}/test_data/numbers_test.py", line 29, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            test_require_failure FAIL
                - requiring a failure stops the test
            """
        ).format(project_root=get_project_root())
        actual = out.getvalue()
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output:\n\n{expected}\ngot:\n\n{actual}",
        )
