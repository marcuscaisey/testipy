import collections
import inspect
from typing import Callable, Any

from .context import TestContext
from .functions import _run_test_function
from .results import PassResult, FailResult, ErrorResult, TestResult, TestResults


class TestClassSetupError(Exception):
    """Raised when an error occurs during test class setup."""

    def __init__(self, raised_error: Exception):
        self.raised_error = raised_error


class TestSetupError(Exception):
    """Raised when an error occurs during test setup."""

    def __init__(self, raised_error: Exception, current_results: TestResults = None):
        self.raised_error = raised_error
        self.current_results = current_results or []


class TestTeardownError(Exception):
    """Raised when an error occurs during test teardown."""

    def __init__(self, raised_error: Exception, current_results: TestResults = None):
        self.raised_error = raised_error
        self.current_results = current_results or []


class TestClassTeardownError(Exception):
    """Raised when an error occurs during test class teardown."""

    def __init__(self, raised_error: Exception, results: TestResults):
        self.raised_error = raised_error
        self.results = results


def _run_test_class(test_class: type) -> TestResult:
    try:
        sub_results = _run_test_methods(test_class)
    except TestClassSetupError as e:
        return ErrorResult(test_class.__name__, error=e.raised_error)
    except TestSetupError as e:
        return ErrorResult(test_class.__name__, error=e.raised_error, sub_results=e.current_results)
    except TestTeardownError as e:
        return ErrorResult(test_class.__name__, error=e.raised_error, sub_results=e.current_results)
    except TestClassTeardownError as e:
        return ErrorResult(test_class.__name__, error=e.raised_error, sub_results=e.results)
    result_type = _get_overall_result_type(sub_results)
    return result_type(test_class.__name__, sub_results=sub_results)


def _run_test_methods(test_class: type) -> TestResults:
    results: list[TestResult] = []
    _setup_class(test_class)
    test_method_names = _get_sorted_test_method_names(test_class)
    for name in test_method_names:
        instance = test_class()
        _setup(instance, current_results=results)
        test_method = getattr(instance, name)
        result = _run_test_function(test_method)
        results.append(result)
        _teardown(instance, current_results=results)
    _teardown_class(test_class, results=results)
    return results


def _setup_class(test_class: type):
    if hasattr(test_class, "setup_class"):
        try:
            test_class.setup_class()
        except Exception as e:
            raise TestClassSetupError(raised_error=e)


def _setup(instance: object, current_results: TestResults):
    if hasattr(instance, "setup"):
        try:
            instance.setup()
        except Exception as e:
            raise TestSetupError(raised_error=e, current_results=current_results)


def _teardown(instance: object, current_results: TestResults):
    if hasattr(instance, "teardown"):
        try:
            instance.teardown()
        except Exception as e:
            raise TestTeardownError(raised_error=e, current_results=current_results)


def _teardown_class(test_class, results: TestResults):
    if hasattr(test_class, "teardown_class"):
        try:
            test_class.teardown_class()
        except Exception as e:
            raise TestClassTeardownError(raised_error=e, results=results)


NameLineNo = collections.namedtuple("NameLineNo", ["name", "line_no"])


def _get_sorted_test_method_names(test_class: type) -> list[str]:
    name_line_no_pairs = [
        NameLineNo(name=name, line_no=_func_definition_line(method))
        for name, method in inspect.getmembers(test_class, predicate=_is_test_method)
    ]
    name_line_no_pairs.sort(key=lambda pair: pair.line_no)
    return [pair.name for pair in name_line_no_pairs]


def _func_definition_line(f: Callable) -> int:
    return f.__code__.co_firstlineno


def _is_test_method(value: Any) -> bool:
    if not inspect.isfunction(value):
        return False
    if not value.__name__.startswith("test_"):
        return False

    sig = inspect.signature(value)
    # should have self and TestContext parameters
    if len(sig.parameters) != 2:
        return False

    parameter = list(sig.parameters.values())[1]
    return parameter.annotation == TestContext


def _get_overall_result_type(results: TestResults) -> type[TestResult]:
    result_type: type[TestResult] = PassResult
    for result in results:
        if isinstance(result, FailResult):
            result_type = FailResult
        elif isinstance(result, ErrorResult):
            result_type = ErrorResult
            break
    return result_type
