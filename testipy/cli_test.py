import io
import unittest

from .cli import testipy
from .common_test import dedent, get_project_root, def_line
from test_data.e2e.exceptions_test import test_exceptions_error_the_test, raises_exception


class TestCLI(unittest.TestCase):
    longMessage = False

    def test_assertions(self):
        actual = self.run_test_file("test_data/e2e/assertions_test.py")

        expected = dedent(
            """
            test_assert_equal FAIL
                - Expected -1 and 5 to be equal; this is most disappointing
            """
        )
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output:\n\n{expected}\ngot:\n\n{actual}",
        )

    def test_exceptions(self):
        actual = self.run_test_file("test_data/e2e/exceptions_test.py")

        expected = dedent(
            """
            test_exceptions_error_the_test ERROR
                Traceback (most recent call last):
                  File "{project_root}/test_data/e2e/exceptions_test.py", line {call_raises_exception_line}, in test_exceptions_error_the_test
                    raises_exception()
                  File "{project_root}/test_data/e2e/exceptions_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            """  # noqa: E501
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_exceptions_error_the_test) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output:\n\n{expected}\ngot:\n\n{actual}",
        )

    def test_failures(self):
        actual = self.run_test_file("test_data/e2e/failures_test.py")

        expected = dedent(
            """
            test_multiple_failures FAIL
                - failure message
                - multiple failures are allowed in the same test
            test_require_failure FAIL
                - requiring a failure stops the test
            """
        )
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output:\n\n{expected}\ngot:\n\n{actual}",
        )

    def test_passing(self):
        actual = self.run_test_file("test_data/e2e/passing_test.py")

        expected = dedent(
            """
            test_passes PASS
            """
        )
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output:\n\n{expected}\ngot:\n\n{actual}",
        )

    def test_classes(self):
        actual = self.run_test_file("test_data/e2e/classes_test.py")

        expected = dedent(
            """
            TestAdd FAIL
            TestAdd/test_adding_two_and_three_returns_five PASS
            TestAdd/test_adding_three_and_three_returns_seven FAIL
                - Expected 7 and 6 to be equal; this is most disappointing
            """
        )
        self.assertEqual(
            expected,
            actual,
            f"expected cli to output:\n\n{expected}\ngot:\n\n{actual}",
        )

    def run_test_file(self, path: str) -> str:
        """Run a test file and return the output."""
        out = io.StringIO()
        testipy(path, out)
        return out.getvalue()
