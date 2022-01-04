import bisect
import io
import textwrap
import traceback as tb
from typing import Callable

from .running import ErrorResult, FailResult, PassResult, TestResults


def format_results_friendly(results: TestResults) -> str:
    """
    Returns the given test results in a human readable format.

    The format for each result is:
        $TEST_NAME (PASS | FAIL | ERROR)
            [$FAILURE_MESSAGES | $ERROR_TRACEBACK]
    Results are sorted in the order of their test definitions.
    """
    formatter = _FriendlyResultsFormatter()
    for result in results.passed:
        formatter.add_pass_result(result)
    for result in results.failed:
        formatter.add_fail_result(result)
    for result in results.errored:
        formatter.add_error_result(result)
    return formatter.print()


class _FriendlyResultsFormatter:
    INDENT_SIZE = 4

    def __init__(self):
        self._formatted_results = []

    def add_pass_result(self, result: PassResult):
        formatted = f"{result.test.__name__} PASS"
        self._insert_result(result.test, formatted)

    def add_fail_result(self, result: FailResult):
        lines = [f"{result.test.__name__} FAIL"]
        lines.extend(self._indent(f"- {message}") for message in result.messages)
        formatted = "\n".join(lines)
        self._insert_result(result.test, formatted)

    def add_error_result(self, result: ErrorResult):
        traceback = self._get_traceback_without_first_stack_trace(result.error)
        lines = [f"{result.test.__name__} ERROR"]
        lines.extend(self._indent(line) for line in traceback.splitlines())
        formatted = "\n".join(lines)
        self._insert_result(result.test, formatted)

    def _insert_result(self, test: Callable, formatted_result: str):
        test_def_line = test.__code__.co_firstlineno
        bisect.insort(self._formatted_results, (test_def_line, formatted_result))

    def print(self) -> str:
        return "\n".join(result for _, result in self._formatted_results) + "\n"

    @classmethod
    def _indent(cls, s: str) -> str:
        return textwrap.indent(s, cls.INDENT_SIZE * " ")

    @staticmethod
    def _get_traceback_without_first_stack_trace(e: Exception) -> str:
        string_io = io.StringIO()
        # __traceback__ is guaranteed to not be None since the exception will
        # always be thrown from inside a test function call meaning that we'll
        # always have a call like test_xxx as the first stack trace entry followed
        # by at least one other entry which is where the exception was actually
        # raised
        next_traceback = e.__traceback__.tb_next
        tb.print_exception(
            type(e),
            value=e,
            tb=next_traceback,
            file=string_io,
        )
        return string_io.getvalue()
