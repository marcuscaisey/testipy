import io
import traceback as tb

from .running import ErrorResult, FailResult, PassResult, TestResults

_INDENT = " " * 4


def format_friendly(results: TestResults) -> str:
    """
    Returns the given test results in a human readable format.

    The format for each result is:
        $TEST_NAME (PASS | FAIL | ERROR)
            [$FAILURE_MESSAGES | $ERROR_TRACEBACK]
    Multiple results are sorted in test order.
    """
    test_order_to_result_lines = {}
    for result in results.passed:
        test_order_to_result_lines[result.test_order] = _pass_result_lines(result)
    for result in results.failed:
        test_order_to_result_lines[result.test_order] = _fail_result_lines(result)
    for result in results.errored:
        test_order_to_result_lines[result.test_order] = _error_result_lines(result)
    sorted_lines = []
    for i in range(1, results.count + 1):
        sorted_lines.extend(test_order_to_result_lines[i])
    return "\n".join(sorted_lines) + "\n"


def _pass_result_lines(result: PassResult) -> list[str]:
    return [f"{result.test_name} PASS"]


def _fail_result_lines(result: FailResult) -> list[str]:
    lines = [f"{result.test_name} FAIL"]
    for message in result.messages:
        lines.append(f"{_INDENT}- {message}")
    return lines


def _error_result_lines(result: ErrorResult) -> list[str]:
    lines = [f"{result.test_name} ERROR"]
    traceback = _get_traceback_without_first_stack_trace(result.error)
    traceback_lines = [f"{_INDENT}{line}" for line in traceback.splitlines()]
    lines.extend(traceback_lines)
    return lines


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
