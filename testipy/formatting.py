import io
import textwrap
import traceback as tb
from typing import Union

from .running import ErrorResult, FailResult, PassResult


class FriendlyResultsFormatter:
    """
    Formats test results in a friendly human-readable way.

    The format for each result is:
        $TEST_NAME (PASS | FAIL | ERROR)
            [$FAILURE_MESSAGES | $ERROR_TRACEBACK]

    Results are sorted in the order of their test definitions.
    """

    # TODO: take this as input as a config parameter instead
    INDENT_SIZE = 4

    def __init__(self, results: list[Union[PassResult, FailResult, ErrorResult]]):
        self._results = results

    def format(self) -> str:
        formatted_results = []
        for result in self._results:
            if isinstance(result, PassResult):
                formatted_results.append(self._format_pass_result(result))
            elif isinstance(result, FailResult):
                formatted_results.append(self._format_fail_result(result))
            elif isinstance(result, ErrorResult):
                formatted_results.append(self._format_error_result(result))
        return "\n".join(formatted_results) + "\n"

    def _format_pass_result(self, result: PassResult) -> str:
        return f"{result.test_name} PASS"

    def _format_fail_result(self, result: FailResult) -> str:
        lines = [f"{result.test_name} FAIL"]
        lines.extend(self._indent(f"- {message}") for message in result.messages)
        return "\n".join(lines)

    def _format_error_result(self, result: ErrorResult) -> str:
        traceback = self._get_traceback_without_first_stack_trace(result.error)
        lines = [f"{result.test_name} ERROR"]
        lines.extend(self._indent(line) for line in traceback.splitlines())
        return "\n".join(lines)

    def _get_traceback_without_first_stack_trace(self, e: Exception) -> str:
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

    def _indent(self, s: str) -> str:
        return textwrap.indent(s, self.INDENT_SIZE * " ")
