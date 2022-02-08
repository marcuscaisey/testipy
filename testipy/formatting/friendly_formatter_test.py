import unittest

from ..running import PassResult, FailResult, ErrorResult
from ..formatting import FriendlyFormatter
from ..common_test import dedent, get_project_root, def_line


class BaseTestCase(unittest.TestCase):
    longMessage = False

    def assertFormattedResultsEqual(self, expected: str, actual: str):
        self.assertEqual(
            expected,
            actual,
            f"expected results to be formatted as:\n\n'{expected}'\ngot:\n\n'{actual}'",
        )


class TestFriendlyFormatter(BaseTestCase):
    longMessage = False

    def test_formats_passing_results_as_a_single_line(self):
        results = [PassResult("test_passes")]

        actual = FriendlyFormatter(results).format()

        expected = "test_passes PASS\n"
        self.assertFormattedResultsEqual(expected, actual)

    def test_formats_failing_results_without_messages_as_a_single_line(self):
        results = [FailResult("test_fails")]

        actual = FriendlyFormatter(results).format()

        expected = "test_fails FAIL\n"
        self.assertFormattedResultsEqual(expected, actual)

    def test_indents_message_on_next_line_when_failing_result_has_message(self):
        results = [FailResult("test_fails", messages=["failure message"])]

        actual = FriendlyFormatter(results).format()

        expected = dedent(
            """
            test_fails FAIL
                - failure message
            """
        )
        self.assertFormattedResultsEqual(expected, actual)

    def test_indents_messages_on_next_line_when_failing_result_has_multiple_messages(self):
        results = [FailResult("test_fails", messages=["failure message 1", "failure message 2"])]

        actual = FriendlyFormatter(results).format()

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

        actual = FriendlyFormatter(results).format()

        expected = dedent(
            """
            test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/formatting/friendly_formatter_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/formatting/friendly_formatter_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
                """  # noqa: E501
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

        actual = FriendlyFormatter(results).format()

        expected = dedent(
            """
            test_passes_1 PASS
            test_fails_1 FAIL
                - failure message
            test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/formatting/friendly_formatter_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/formatting/friendly_formatter_test.py", line {raise_value_error_line}, in raises_exception
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
        self.assertFormattedResultsEqual(expected, actual)


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

        actual = FriendlyFormatter(results).format()

        expected = dedent(
            """
            TestFoo PASS
            TestFoo/test_passes_1 PASS
            TestFoo/test_passes_2 PASS
            """
        )
        self.assertFormattedResultsEqual(expected, actual)

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

        actual = FriendlyFormatter(results).format()

        expected = dedent(
            """
            TestFoo FAIL
            TestFoo/test_passes PASS
            TestFoo/test_fails FAIL
                - oh no!
            """
        )
        self.assertFormattedResultsEqual(expected, actual)

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

        actual = FriendlyFormatter(results).format()

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
        self.assertFormattedResultsEqual(expected, actual)

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

        actual = FriendlyFormatter(results).format()

        expected = dedent(
            """
            TestFoo ERROR
            TestFoo/test_passes PASS
            TestFoo/test_fails FAIL
                - oh no!
            TestFoo/test_errors ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/formatting/friendly_formatter_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/formatting/friendly_formatter_test.py", line {raise_value_error_line}, in raises_exception
                    raise ValueError("oh no!")
                ValueError: oh no!
            """  # noqa: E501
        ).format(
            project_root=get_project_root(),
            call_raises_exception_line=def_line(test_errors) + 1,
            raise_value_error_line=def_line(raises_exception) + 1,
        )
        self.assertFormattedResultsEqual(expected, actual)

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

        actual = FriendlyFormatter(results).format()

        expected = dedent(
            """
            TestFoo ERROR
                Traceback (most recent call last):
                  File "{project_root}/testipy/formatting/friendly_formatter_test.py", line {call_raises_exception_line}, in test_errors
                    raises_exception()
                  File "{project_root}/testipy/formatting/friendly_formatter_test.py", line {raise_value_error_line}, in raises_exception
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
        self.assertFormattedResultsEqual(expected, actual)
