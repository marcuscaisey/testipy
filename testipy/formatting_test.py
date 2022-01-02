import unittest

from .running import TestResult
from .formatting import format_friendly
from .common_test import dedent, get_project_root


class TestFormatFriendly(unittest.TestCase):
    longMessage = False

    def assertFormattedResultsEqual(self, results: list[TestResult], expected: str, actual: str):
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as:\n\n{expected}\ngot:\n\n{actual}",
        )

    def test_formats_passing_results_as_a_single_line(self):
        results = [
            TestResult("test_passes", is_pass=True),
        ]

        actual = format_friendly(results)

        expected = "test_passes PASS\n"
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_formats_failing_results_without_messages_as_a_single_line(self):
        results = [
            TestResult("test_fails", is_pass=False),
        ]

        actual = format_friendly(results)

        expected = "test_fails FAIL\n"
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_indents_message_on_next_line_when_failing_result_has_message(self):
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

    def test_indents_messages_on_next_line_when_failing_result_has_multiple_messages(self):
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

    def test_formats_errored_results_as_traceback_without_first_stack_trace_entry(self):
        def test_errors():
            raises_exception()

        def raises_exception():
            raise ValueError("oh no!")

        try:
            test_errors()
        except ValueError as e:
            error = e

        results = [TestResult("test_errors", is_pass=False, error=error)]

        actual = format_friendly(results)

        expected = dedent(
            """
            test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/formatting_test.py", line 78, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/formatting_test.py", line 81, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            """
        ).format(project_root=get_project_root())
        self.assertFormattedResultsEqual(results, expected, actual)

    # def test_formats_multiple_results_as_multiple_lines(self):
    #     def test_errors():
    #         raises_exception()

    #     def raises_exception():
    #         raise ValueError("oh no!")

    #     try:
    #         test_errors()
    #     except ValueError as e:
    #         error = e

    #     results = [
    #         TestResult("test_passes_1", is_pass=True),
    #         TestResult("test_fails_1", is_pass=False, messages=["failure message"]),
    #         TestResult("test_errors", is_pass=False, error=error),
    #         TestResult("test_passes_2", is_pass=True),
    #         TestResult("test_fails_2", is_pass=False),
    #     ]

    #     actual = format_friendly(results)

    #     expected = dedent(
    #         """
    #         test_passes_1 PASS
    #         test_fails_1 FAIL
    #             - failure message
    #         test_errors ERROR
    #             Traceback (most recent call last):
    #               File "{project_root}/testipy/formatting_test.py", line 104, in test_errors
    #                 raises_exception()
    #               File "{project_root}/testipy/formatting_test.py", line 107, in raises_exception
    #                 raise ValueError("oh no!")
    #             ValueError: oh no!
    #         test_passes_2 PASS
    #         test_fails_2 FAIL
    #         """
    #     ).format(project_root=get_project_root())
    #     self.assertFormattedResultsEqual(results, expected, actual)
