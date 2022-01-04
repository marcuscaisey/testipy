import io
import unittest

from .cli import testipy
from .common_test import dedent, get_project_root, def_line
from test_data.numbers_test import test_exceptions_error_the_test, raises_exception


class TestCLI(unittest.TestCase):
    longMessage = False

    def test_cli_with_simple_test_file(self):
        out = io.StringIO()
        testipy("test_data/numbers_test.py", out)

        expected = dedent(
            """
            test_add PASS
            test_sub FAIL
                - Expected -1 and 5 to be equal; this is most disappointing
            test_multiple_failures FAIL
                - failure message
                - multiple failures are allowed in the same test
            test_exceptions_error_the_test ERROR
                Traceback (most recent call last):
                  File "{project_root}/test_data/numbers_test.py", line {call_raises_exception_line}, in test_exceptions_error_the_test
                    raises_exception()
                  File "{project_root}/test_data/numbers_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            test_require_failure FAIL
                - requiring a failure stops the test
            """
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_exceptions_error_the_test) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        actual = out.getvalue()
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output:\n\n{expected}\ngot:\n\n{actual}",
        )
