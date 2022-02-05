from __future__ import annotations
import collections
import dataclasses
import inspect
from typing import Any, Callable, Iterable, Union, Optional


class StopTest(Exception):
    """Raised to signal that the current test should be stopped."""

    pass


class TestContext:
    """Object made available inside tests to manage test state."""

    def __init__(self):
        self._passed = True
        self._messages = []

    def fail(self, message: str = "", *, require: bool = False):
        """Fail the current test, optionally with a given failure message."""
        self._passed = False
        if message:
            self._messages.append(message)
        if require:
            raise StopTest()

    def assert_equal(self, expected: Any, actual: Any, message: str = "", *, require: bool = False):
        """Assert that expected and actual are equal, failing the test if not."""
        if expected != actual:
            failure_message = f"Expected {expected} and {actual} to be equal"
            if message:
                failure_message += f"; {message}"
            self.fail(failure_message, require=require)


TestFunction = Callable[[TestContext], None]


@dataclasses.dataclass
class PassResult:
    test_name: str
    _: dataclasses.KW_ONLY
    sub_results: list[PassResult] = dataclasses.field(default_factory=list)

    def __repr__(self) -> str:
        args = [repr(self.test_name)]
        if self.sub_results:
            args.append(f"sub_results={repr(self.sub_results)}")
        joined_args = ", ".join(args)
        return f"PassResult({joined_args})"


@dataclasses.dataclass
class FailResult:
    test_name: str
    _: dataclasses.KW_ONLY
    messages: list[str] = dataclasses.field(default_factory=list)
    sub_results: list[Union[PassResult, FailResult]] = dataclasses.field(default_factory=list)

    def __repr__(self) -> str:
        args = [repr(self.test_name)]
        if self.messages:
            args.append(f"messages={repr(self.messages)}")
        if self.sub_results:
            args.append(f"sub_results={repr(self.sub_results)}")
        joined_args = ", ".join(args)
        return f"FailResult({joined_args})"


@dataclasses.dataclass
class ErrorResult:
    test_name: str
    _: dataclasses.KW_ONLY
    error: Optional[Exception] = None
    sub_results: list[Union[PassResult, FailResult, ErrorResult]] = dataclasses.field(
        default_factory=list
    )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ErrorResult):
            return False
        if self.test_name != other.test_name or self.sub_results != other.sub_results:
            return False
        if self.error and other.error:
            return self.error.args == other.error.args
        return not self.error and not other.error

    def __repr__(self) -> str:
        args = [repr(self.test_name)]
        if self.error:
            args.append(f"error={repr(self.error)}")
        if self.sub_results:
            args.append(f"sub_results={repr(self.sub_results)}")
        joined_args = ", ".join(args)
        return f"ErrorResult({joined_args})"


TestResult = Union[PassResult, FailResult, ErrorResult]
TestResults = list[TestResult]


def run_tests(tests: Iterable[Union[TestFunction, type]]) -> TestResults:
    """Runs some test functions and test classes and returns their result."""
    results: TestResults = []
    for test in tests:
        if inspect.isfunction(test):
            test_function = test
            result = _run_test_function(test_function)
            results.append(result)

        elif inspect.isclass(test):
            test_class = test
            sub_results = _run_test_class(test_class)
            result_type = _get_overall_result_type(sub_results)
            results.append(result_type(test_class.__name__, sub_results=sub_results))

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
    results: TestResults = []
    test_method_names = _get_sorted_test_method_names(test_class)
    for name in test_method_names:
        instance = test_class()
        test_method = getattr(instance, name)
        result = _run_test_function(test_method)
        results.append(result)
    return results


NameLineNo = collections.namedtuple("TestMethodNameLinNo", ["name", "line_no"])


def _get_sorted_test_method_names(test_class: type) -> list[TestFunction]:
    name_line_no_pairs = [
        NameLineNo(name=name, line_no=_func_definition_line(method))
        for name, method in inspect.getmembers(test_class, predicate=_is_test_method)
    ]
    name_line_no_pairs.sort(key=lambda pair: pair.line_no)
    return [pair.name for pair in name_line_no_pairs]


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


def _func_definition_line(f: Callable) -> int:
    return f.__code__.co_firstlineno


def _get_overall_result_type(results: TestResults) -> type[TestResult]:
    result_type: type[TestResult] = PassResult
    for result in results:
        if isinstance(result, FailResult):
            result_type = FailResult
        elif isinstance(result, ErrorResult):
            result_type = ErrorResult
            break
    return result_type
