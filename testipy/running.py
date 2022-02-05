from __future__ import annotations
import dataclasses
from typing import Any, Callable, Iterable


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
    """
    The result of a passing test.

    Attributes:
        test_name: The name of the test.
        run_order: The order that the test was run in.
    """

    test_name: str
    _: dataclasses.KW_ONLY
    run_order: int = 1


@dataclasses.dataclass
class FailResult:
    """
    The result of a failing test.

    Attributes:
        test_name: The name of the test.
        run_order: The order that the test was run in.
        messages: The failure messages added during the test run.
    """

    test_name: str
    _: dataclasses.KW_ONLY
    run_order: int = 1
    messages: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ErrorResult:
    """
    The result of an errored test.

    Attributes:
        name: The name of the test.
        order: The order that the test was run in.
        error: The exception that was raised during the test run.
    """

    test_name: str
    _: dataclasses.KW_ONLY
    run_order: int = 1
    error: Exception

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.test_name == other.test_name and self.error.args == other.error.args


@dataclasses.dataclass
class TestResults:
    """
    The results of a group of tests that have been run together.

    Attributes:
        passed: The results of the tests that passed.
        failed: The results of the tests that failed.
        errored: The results of the tests that errored.
    """

    _: dataclasses.KW_ONLY
    passed: list[PassResult] = dataclasses.field(default_factory=list)
    failed: list[FailResult] = dataclasses.field(default_factory=list)
    errored: list[ErrorResult] = dataclasses.field(default_factory=list)

    @property
    def count(self) -> int:
        """The total number of tests results."""
        return len(self.passed) + len(self.failed) + len(self.errored)


def run_tests(tests: Iterable[TestFunction]) -> TestResults:
    """
    Runs some tests functions and returns the result of each test.

    Test functions are ones which accept a single TestContext argument. The
    TestContext is used to make assertions and signal test failures. Tests
    which do not fail any assertions, call fail on the TestContext, or raise an
    exception are deemed to have passed.
    """
    results = TestResults()
    for run_order, test in enumerate(tests, 1):
        t = TestContext()
        try:
            test(t)
        except StopTest:
            pass
        except Exception as e:
            results.errored.append(ErrorResult(test.__name__, run_order=run_order, error=e))
            continue
        if t._passed:
            results.passed.append(PassResult(test.__name__, run_order=run_order))
        else:
            results.failed.append(
                FailResult(test.__name__, run_order=run_order, messages=t._messages)
            )
    return results
