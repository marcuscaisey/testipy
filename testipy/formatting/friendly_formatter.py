import io
import textwrap
import traceback as tb

from ..running import ErrorResult, FailResult, PassResult, TestResults


class FriendlyFormatter:
    # TODO: update this to be accurate
    """
    Formats test results in a friendly human-readable way.

    The format for each result is:
        $TEST_NAME (PASS | FAIL | ERROR)
            [$FAILURE_MESSAGES | $ERROR_TRACEBACK]
    """

    # TODO: take this as input as a config parameter instead
    INDENT_SIZE = 4

    def __init__(self, results: TestResults, test_prefix: str = ""):
        self._results = results
        self._test_prefix = test_prefix

    def format(self, *, trailing_new_line=True) -> str:
        formatted_results = []
        for result in self._results:
            if isinstance(result, PassResult):
                formatted_results.append(self._format_pass_result(result))
            elif isinstance(result, FailResult):
                formatted_results.append(self._format_fail_result(result))
            elif isinstance(result, ErrorResult):
                formatted_results.append(self._format_error_result(result))
        formatted = "\n".join(formatted_results)
        if trailing_new_line:
            formatted += "\n"
        return formatted

    def _format_pass_result(self, result: PassResult) -> str:
        lines = [f"{self._test_prefix}{result.test_name} PASS"]
        lines.extend(self._format_sub_results(result.test_name, result.sub_results))
        return "\n".join(lines)

    def _format_fail_result(self, result: FailResult) -> str:
        lines = [f"{self._test_prefix}{result.test_name} FAIL"]
        lines.extend(self._indent(f"- {message}") for message in result.messages)
        lines.extend(self._format_sub_results(result.test_name, result.sub_results))
        return "\n".join(lines)

    def _format_error_result(self, result: ErrorResult) -> str:
        lines = [f"{self._test_prefix}{result.test_name} ERROR"]
        if result.error:
            traceback = self._get_traceback_without_first_stack_trace(result.error)
            lines.extend(self._indent(line) for line in traceback.splitlines())
        lines.extend(self._format_sub_results(result.test_name, result.sub_results))
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

    def _format_sub_results(self, test_name: str, sub_results: TestResults) -> list[str]:
        lines: list[str] = []
        if sub_results:
            formatter = FriendlyFormatter(sub_results, test_prefix=test_name + "/")
            formatted = formatter.format(trailing_new_line=False)
            lines.append(formatted)
        return lines
