import unittest

from .running import TestResult
from .formatting import format_friendly
from .common_test import dedent


class TestFormatFriendly(unittest.TestCase):
    longMessage = False

    def assertFormattedResultsEqual(self, results: list[TestResult], expected: str, actual: str):
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as:\n\n{expected}\ngot:\n\n{actual}",
        )

    def test_formats_a_single_passing_result_on_one_line(self):
        results = [
            TestResult("test_passes", is_pass=True),
        ]

        actual = format_friendly(results)

        expected = "test_passes PASS\n"
        self.assertFormattedResultsEqual(results, expected, actual)

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
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_formats_a_single_failing_result_on_one_line(self):
        results = [
            TestResult("test_fails", is_pass=False),
        ]

        actual = format_friendly(results)

        expected = "test_fails FAIL\n"
        self.assertFormattedResultsEqual(results, expected, actual)

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
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_indents_message_on_next_line_when_failing_results_have_message(self):
        results = [
            TestResult("test_fails", is_pass=False, messages=["failure message"]),
        ]

        actual = format_friendly(results)

        expected = dedent(
            """
            test_fails FAIL
                - failure message
            """
        )
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_indents_messages_on_next_line_when_failing_results_have_multiple_messages(self):
        results = [
            TestResult(
                "test_fails",
                is_pass=False,
                messages=[
                    "failure message 1",
                    "failure message 2",
                ],
            ),
        ]

        actual = format_friendly(results)

        expected = dedent(
            """
            test_fails FAIL
                - failure message 1
                - failure message 2
            """
        )
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_formats_passing_and_failing_results_as_multiple_lines(self):
        results = [
            TestResult("test_passes_1", is_pass=True),
            TestResult("test_fails_1", is_pass=False, messages=["failure message"]),
            TestResult("test_passes_2", is_pass=True),
            TestResult("test_fails_2", is_pass=False),
        ]

        actual = format_friendly(results)

        expected = dedent(
            """
            test_passes_1 PASS
            test_fails_1 FAIL
                - failure message
            test_passes_2 PASS
            test_fails_2 FAIL
            """
        )
        self.assertFormattedResultsEqual(results, expected, actual)
