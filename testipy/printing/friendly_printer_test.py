import io
import unittest

from testipy.running.results import TestResults

from ..running import PassResult, FailResult, ErrorResult
from ..printing import FriendlyPrinter
from ..common_test import dedent, get_project_root, def_line


class BaseTestCase(unittest.TestCase):
    longMessage = False

    def assertPrintedResultsEqual(self, expected: str, actual: str):
        self.assertEqual(
            expected,
            actual,
            f"expected results to be formatted as:\n\n'{expected}'\ngot:\n\n'{actual}'",
        )

    def print_results_to_string(self, *args, **kwargs) -> str:
        out = io.StringIO()
        FriendlyPrinter(*args, **kwargs).print(out=out)
        return out.getvalue()


class TestFriendlyPrinter(BaseTestCase):
    longMessage = False

    def test_formats_passing_results_as_a_single_line(self):
        results = [PassResult("test_passes")]

        actual = self.print_results_to_string(results)

        expected = "test_passes PASS\n"
        self.assertPrintedResultsEqual(expected, actual)

    def test_formats_failing_results_without_messages_as_a_single_line(self):
        results = [FailResult("test_fails")]

        actual = self.print_results_to_string(results)

        expected = "test_fails FAIL\n"
        self.assertPrintedResultsEqual(expected, actual)

    def test_indents_message_on_next_line_when_failing_result_has_message(self):
        results = [FailResult("test_fails", messages=["failure message"])]

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            test_fails FAIL
                - failure message
            """
        )
        self.assertPrintedResultsEqual(expected, actual)

    def test_indents_messages_on_next_line_when_failing_result_has_multiple_messages(self):
        results = [FailResult("test_fails", messages=["failure message 1", "failure message 2"])]

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            test_fails FAIL
                - failure message 1
                - failure message 2
            """
        )
        self.assertPrintedResultsEqual(expected, actual)

    def test_indents_with_given_indent_size(self):
        results = [FailResult("test_fails", messages=["failure message 1", "failure message 2"])]

        actual = self.print_results_to_string(results, indent_size=7)

        expected = dedent(
            """
            test_fails FAIL
                   - failure message 1
                   - failure message 2
            """
        )
        self.assertPrintedResultsEqual(expected, actual)

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

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/printing/friendly_printer_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/printing/friendly_printer_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            """  # noqa: E501
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_errors) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        self.assertPrintedResultsEqual(expected, actual)

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

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            test_passes_1 PASS
            test_fails_1 FAIL
                - failure message
            test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/printing/friendly_printer_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/printing/friendly_printer_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            test_passes_2 PASS
            test_fails_2 FAIL
            """  # noqa: E501
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_errors) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        self.assertPrintedResultsEqual(expected, actual)


class TestSubResults(BaseTestCase):
    def test_formats_pass_result_with_sub_results_indented(self):
        results = [
            PassResult(
                "TestFoo",
                sub_results=[
                    PassResult("test_passes_1"),
                    PassResult("test_passes_2"),
                ],
            )
        ]

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            TestFoo PASS
            TestFoo/test_passes_1 PASS
            TestFoo/test_passes_2 PASS
            """
        )
        self.assertPrintedResultsEqual(expected, actual)

    def test_formats_fail_result_with_sub_results_indented(self):
        results = [
            FailResult(
                "TestFoo",
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["oh no!"]),
                ],
            )
        ]

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            TestFoo FAIL
            TestFoo/test_passes PASS
            TestFoo/test_fails FAIL
                - oh no!
            """
        )
        self.assertPrintedResultsEqual(expected, actual)

    def test_formats_fail_result_messages_before_sub_results(self):
        results = [
            FailResult(
                "TestFoo",
                messages=["message 1", "message 2"],
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["oh no!"]),
                ],
            )
        ]

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            TestFoo FAIL
                - message 1
                - message 2
            TestFoo/test_passes PASS
            TestFoo/test_fails FAIL
                - oh no!
            """
        )
        self.assertPrintedResultsEqual(expected, actual)

    def test_formats_error_result_with_sub_results_indented(self):
        def test_errors():
            raises_exception()

        def raises_exception():
            raise ValueError("oh no!")

        try:
            test_errors()
        except ValueError as e:
            error = e

        results = [
            ErrorResult(
                "TestFoo",
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["oh no!"]),
                    ErrorResult("test_errors", error=error),
                ],
            )
        ]

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            TestFoo ERROR
            TestFoo/test_passes PASS
            TestFoo/test_fails FAIL
                - oh no!
            TestFoo/test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/printing/friendly_printer_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/printing/friendly_printer_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            """  # noqa: E501
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_errors) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        self.assertPrintedResultsEqual(expected, actual)

    def test_formats_error_result_error_traceback_after_sub_results(self):
        def test_errors():
            raises_exception()

        def raises_exception():
            raise ValueError("oh no!")

        try:
            test_errors()
        except ValueError as e:
            error = e

        results = [
            ErrorResult(
                "TestFoo",
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["oh no!"]),
                ],
                error=error,
            )
        ]

        actual = self.print_results_to_string(results)

        expected = dedent(
            """
            TestFoo ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/printing/friendly_printer_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/printing/friendly_printer_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            TestFoo/test_passes PASS
            TestFoo/test_fails FAIL
                - oh no!
            """  # noqa: E501
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_errors) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        self.assertPrintedResultsEqual(expected, actual)
