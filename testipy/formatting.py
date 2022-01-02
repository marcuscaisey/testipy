import io
import traceback as tb

from .running import TestResult

_INDENT = " " * 4


def format_friendly(results: list[TestResult]) -> str:
    """
    Returns the given test results in a human readable format.

    The format for each result is:
        $TEST_NAME (PASS | FAIL | ERROR)
            [$FAILURE_MESSAGES | $ERROR_TRACEBACK]
    """
    lines = []
    for result in results:
        if result.is_pass:
            status = "PASS"
        elif result.error is not None:
            status = "ERROR"
        else:
            status = "FAIL"
        lines.append(f"{result.test_name} {status}")
        for message in result.messages:
            lines.append(f"{_INDENT}- {message}")
        if result.error is not None:
            traceback = _get_traceback_without_first_stack_trace(result.error)
            traceback_lines = [f"{_INDENT}{line}" for line in traceback.splitlines()]
            lines.extend(traceback_lines)
    return "\n".join(lines) + "\n"


def _get_traceback_without_first_stack_trace(e: Exception) -> str:
    string_io = io.StringIO()
    next_traceback = e.__traceback__.tb_next
    tb.print_exception(
        type(e),
        value=e,
        tb=next_traceback,
        file=string_io,
    )
    return string_io.getvalue()
