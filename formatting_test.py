import textwrap
import unittest

from running import TestResult
from formatting import format_friendly


class TestFormatFriendly(unittest.TestCase):
    longMessage = False

    def test_formats_a_single_passing_result_on_one_line(self):
        results = [
            TestResult("test_passes", is_pass=True),
        ]

        actual = format_friendly(results)

        expected = "test_passes PASS"
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as \n'{expected}', \ngot \n'{actual}'",
        )

    def test_formats_multiple_passing_results_as_multiple_lines(self):
        results = [
            TestResult("test_passes_1", is_pass=True),
            TestResult("test_passes_2", is_pass=True),
        ]

        actual = format_friendly(results)

        expected = dedent(
            """
            test_passes_1 PASS
            test_passes_2 PASS
            """
        )
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as \n'{expected}', \ngot \n'{actual}'",
        )

    def test_formats_a_single_failing_result_on_one_line(self):
        results = [
            TestResult("test_fails", is_pass=False),
        ]

        actual = format_friendly(results)

        expected = "test_fails FAIL"
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as \n'{expected}', \ngot \n'{actual}'",
        )

    def test_formats_multiple_failing_results_as_multiple_lines(self):
        results = [
            TestResult("test_fails_1", is_pass=False),
            TestResult("test_fails_2", is_pass=False),
        ]

        actual = format_friendly(results)

        expected = dedent(
            """
            test_fails_1 FAIL
            test_fails_2 FAIL
            """
        )
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as \n'{expected}', \ngot \n'{actual}'",
        )

    def test_indents_message_on_next_line_when_failing_results_have_message(self):
        results = [
            TestResult("test_fails", is_pass=False, message="failure message"),
        ]

        actual = format_friendly(results)

        expected = dedent(
            """
            test_fails FAIL
                failure message
            """
        )
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as \n'{expected}', \ngot \n'{actual}'",
        )

    def test_formats_passing_and_failing_results_as_multiple_lines(self):
        results = [
            TestResult("test_passes_1", is_pass=True),
            TestResult("test_fails_1", is_pass=False, message="failure message"),
            TestResult("test_passes_2", is_pass=True),
            TestResult("test_fails_2", is_pass=False),
        ]

        actual = format_friendly(results)

        expected = dedent(
            """
            test_passes_1 PASS
            test_fails_1 FAIL
                failure message
            test_passes_2 PASS
            test_fails_2 FAIL
            """
        )
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as \n'{expected}', \ngot \n'{actual}'",
        )


def dedent(s: str) -> str:
    return textwrap.dedent(s).strip()
