import io
import sys
import textwrap
import traceback as tb
from typing import TextIO

from rich import console

from ..running import ErrorResult, FailResult, PassResult, TestResults


class NoNextTracebackError(Exception):
    pass


class FriendlyPrinter:
    # TODO: update this to be accurate
    """
    Prints test results in a friendly human-readable way.

    The format for each result is:
        $TEST_NAME (PASS | FAIL | ERROR)
            [$FAILURE_MESSAGES | $ERROR_TRACEBACK]
    """

    def __init__(self, results: TestResults, *, colourise: bool = True, indent_size: int = 4):
        self._results = results
        self._colourise = colourise
        self._indent_size = indent_size
        self._tests_run = 0
        self._tests_passed = 0
        self._tests_failed = 0
        self._tests_errored = 0

    def print(self, *, out: TextIO = sys.stdout):
        formatted = self._format(self._results)
        c = console.Console(file=out)
        c.print(formatted, highlight=False)
        c.print(self._summary(), highlight=False)

    def _format(self, results: TestResults, prefix: str = "") -> str:
        formatted_results = []
        for result in results:
            self._tests_run += 1
            if isinstance(result, PassResult):
                self._tests_passed += 1
                formatted_results.append(self._format_pass_result(result, prefix))
            elif isinstance(result, FailResult):
                self._tests_failed += 1
                formatted_results.append(self._format_fail_result(result, prefix))
            elif isinstance(result, ErrorResult):
                self._tests_errored += 1
                formatted_results.append(self._format_error_result(result, prefix))
        formatted = "\n".join(formatted_results)
        return formatted

    def _format_pass_result(self, result: PassResult, test_prefix: str = "") -> str:
        lines = [self._format_test_name(result.test_name, "PASS", test_prefix, style="green bold")]
        lines.extend(self._format_sub_results(result.test_name, result.sub_results))
        return "\n".join(lines)

    def _format_fail_result(self, result: FailResult, test_prefix: str = "") -> str:
        lines = [self._format_test_name(result.test_name, "FAIL", test_prefix, style="red bold")]
        lines.extend(self._indent(f"- {message}") for message in result.messages)
        lines.extend(self._format_sub_results(result.test_name, result.sub_results))
        return "\n".join(lines)

    def _format_error_result(self, result: ErrorResult, test_prefix: str = "") -> str:
        lines = [self._format_test_name(result.test_name, "ERROR", test_prefix, style="blue bold")]
        if result.error:
            traceback = self._get_traceback_without_first_stack_trace(result.error)
            lines.extend(self._indent(line) for line in traceback.splitlines())
        lines.extend(self._format_sub_results(result.test_name, result.sub_results))
        return "\n".join(lines)

    def _format_test_name(self, test_name: str, result: str, test_prefix: str, style: str) -> str:
        formatted = f"{test_name} {result}"
        if test_prefix:
            formatted = f"{test_prefix}/{formatted}"
        if self._colourise and style:
            formatted = self._style(formatted, style)
        return formatted

    def _style(self, s: str, style: str) -> str:
        return f"[{style}]{s}[/{style}]"

    def _format_sub_results(self, test_name: str, sub_results: TestResults) -> list[str]:
        lines: list[str] = []
        if sub_results:
            formatted = self._format(sub_results, prefix=test_name)
            lines.append(formatted)
        return lines

    def _get_traceback_without_first_stack_trace(self, e: Exception) -> str:
        string_io = io.StringIO()
        # __traceback__ is guaranteed to not be None since the exception will
        # always be thrown from inside a test function call meaning that we'll
        # always have a call like test_xxx as the first stack trace entry followed
        # by at least one other entry which is where the exception was actually
        # raised
        if not e.__traceback__:
            raise NoNextTracebackError(
                f"Expected traceback {e.__traceback__} to have another traceback chained on to it."
            )
        next_traceback = e.__traceback__.tb_next
        tb.print_exception(
            type(e),
            value=e,
            tb=next_traceback,
            file=string_io,
        )
        return string_io.getvalue()

    def _indent(self, s: str) -> str:
        return textwrap.indent(s, self._indent_size * " ")

    def _summary(self) -> str:
        plural = "s" if self._tests_run > 1 else ""
        summary = f"{self._tests_run} test{plural} run;"
        parts = []
        if self._tests_passed:
            parts.append(self._style(f"{self._tests_passed} passed", "green"))
        if self._tests_failed:
            parts.append(self._style(f"{self._tests_failed} failed", "red"))
        if self._tests_errored:
            parts.append(self._style(f"{self._tests_errored} errored", "blue"))
        summary += " " + ", ".join(parts)
        return self._style(summary, "bold")
