import unittest

from .running import TestResult, TestResults, PassResult, FailResult, ErrorResult
from .formatting import format_friendly
from .common_test import dedent, get_project_root, def_line


class TestFormatFriendly(unittest.TestCase):
    longMessage = False

    def test_formats_passing_results_as_a_single_line(self):
        results = TestResults(
            passed=[PassResult(1, "test_passes")],
        )

        actual = format_friendly(results)

        expected = "test_passes PASS\n"
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_formats_failing_results_without_messages_as_a_single_line(self):
        results = TestResults(
            failed=[FailResult(1, "test_fails")],
        )

        actual = format_friendly(results)

        expected = "test_fails FAIL\n"
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_indents_message_on_next_line_when_failing_result_has_message(self):
        results = TestResults(
            failed=[FailResult(1, "test_fails", messages=["failure message"])],
        )

        actual = format_friendly(results)

        expected = dedent(
            """
            test_fails FAIL
                - failure message
            """
        )
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_indents_messages_on_next_line_when_failing_result_has_multiple_messages(self):
        results = TestResults(
            failed=[
                FailResult(1, "test_fails", messages=["failure message 1", "failure message 2"])
            ],
        )

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

        results = TestResults(
            errored=[ErrorResult(1, "test_errors", error)],
        )

        actual = format_friendly(results)

        expected = dedent(
            """
            test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/formatting_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/formatting_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            """
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_errors) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        self.assertFormattedResultsEqual(results, expected, actual)

    def test_formats_multiple_results_as_multiple_lines_sorted_by_test_order(self):
        def test_errors():
            raises_exception()

        def raises_exception():
            raise ValueError("oh no!")

        try:
            test_errors()
        except ValueError as e:
            error = e

        results = TestResults(
            passed=[
                PassResult(1, "test_passes_1"),
                PassResult(4, "test_passes_2"),
            ],
            failed=[
                FailResult(2, "test_fails_1", messages=["failure message"]),
                FailResult(5, "test_fails_2"),
            ],
            errored=[ErrorResult(3, "test_errors", error)],
        )

        actual = format_friendly(results)

        expected = dedent(
            """
            test_passes_1 PASS
            test_fails_1 FAIL
                - failure message
            test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/formatting_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/formatting_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            test_passes_2 PASS
            test_fails_2 FAIL
            """
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_errors) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        self.assertFormattedResultsEqual(results, expected, actual)

    def assertFormattedResultsEqual(self, results: TestResults, expected: str, actual: str):
        self.assertEqual(
            expected,
            actual,
            f"expected {results} to be formatted as:\n\n{expected}\ngot:\n\n{actual}",
        )
