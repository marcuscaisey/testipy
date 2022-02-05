import unittest

from .running import PassResult, FailResult, ErrorResult
from .formatting import FriendlyResultsFormatter
from .common_test import dedent, get_project_root, def_line


class TestFriendlyResultsFormatter(unittest.TestCase):
    longMessage = False

    def test_formats_passing_results_as_a_single_line(self):
        results = [PassResult("test_passes")]

        actual = FriendlyResultsFormatter(results).format()

        expected = "test_passes PASS\n"
        self.assertFormattedResultsEqual(expected, actual)

    def test_formats_failing_results_without_messages_as_a_single_line(self):
        results = [FailResult("test_fails")]

        actual = FriendlyResultsFormatter(results).format()

        expected = "test_fails FAIL\n"
        self.assertFormattedResultsEqual(expected, actual)

    def test_indents_message_on_next_line_when_failing_result_has_message(self):
        results = [FailResult("test_fails", messages=["failure message"])]

        actual = FriendlyResultsFormatter(results).format()

        expected = dedent(
            """
            test_fails FAIL
                - failure message
            """
        )
        self.assertFormattedResultsEqual(expected, actual)

    def test_indents_messages_on_next_line_when_failing_result_has_multiple_messages(self):
        results = [FailResult("test_fails", messages=["failure message 1", "failure message 2"])]

        actual = FriendlyResultsFormatter(results).format()

        expected = dedent(
            """
            test_fails FAIL
                - failure message 1
                - failure message 2
            """
        )
        self.assertFormattedResultsEqual(expected, actual)

    def test_formats_errored_results_as_traceback_without_first_stack_trace_entry(self):
        # FIXME: find cleaner way to generate traceback for testing with
        def test_errors():
            raises_exception()

        def raises_exception():
            raise ValueError("oh no!")

        try:
            test_errors()
        except ValueError as e:
            error = e

        results = [ErrorResult("test_errors", error=error)]

        actual = FriendlyResultsFormatter(results).format()

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
        self.assertFormattedResultsEqual(expected, actual)

    def test_formats_multiple_results_as_multiple_lines_in_same_order(self):
        def test_errors():
            raises_exception()

        def raises_exception():
            raise ValueError("oh no!")

        try:
            test_errors()
        except ValueError as e:
            error = e

        results = [
            PassResult("test_passes_1"),
            FailResult("test_fails_1", messages=["failure message"]),
            ErrorResult("test_errors", error=error),
            PassResult("test_passes_2"),
            FailResult("test_fails_2"),
        ]

        actual = FriendlyResultsFormatter(results).format()

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
        self.assertFormattedResultsEqual(expected, actual)

    def assertFormattedResultsEqual(self, expected: str, actual: str):
        self.assertEqual(
            expected,
            actual,
            f"expected results to be formatted as:\n\n'{expected}'\ngot:\n\n'{actual}'",
        )
