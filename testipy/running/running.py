from __future__ import annotations
import collections
import inspect
from typing import Any, Callable, Iterable, Union

from .context import TestContext, StopTest
from .results import PassResult, FailResult, ErrorResult, TestResult, TestResults


TestFunction = Callable[[TestContext], None]


def run_tests(tests: Iterable[Union[TestFunction, type]]) -> TestResults:
    """Runs some test functions and test classes and returns their result."""
    results: list[TestResult] = []
    for test in tests:
        if inspect.isfunction(test):
            test_function = test
            result = _run_test_function(test_function)
            results.append(result)

        elif inspect.isclass(test):
            test_class = test
            sub_results = _run_test_class(test_class)
            result_type = _get_overall_result_type(sub_results)
            results.append(result_type(test_class.__name__, sub_results=sub_results))  # type: ignore[arg-type]

    return results


def _run_test_function(f: TestFunction) -> TestResult:
    t = TestContext()
    try:
        f(t)
    except StopTest:
        pass
    except Exception as e:
        return ErrorResult(f.__name__, error=e)
    if not t._passed:
        return FailResult(f.__name__, messages=t._messages)
    return PassResult(f.__name__)


def _run_test_class(test_class: type) -> TestResults:
    results: list[TestResult] = []
    test_method_names = _get_sorted_test_method_names(test_class)
    for name in test_method_names:
        instance = test_class()
        test_method = getattr(instance, name)
        result = _run_test_function(test_method)
        results.append(result)
    return results


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
