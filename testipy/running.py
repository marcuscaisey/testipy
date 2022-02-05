from __future__ import annotations
import dataclasses
from typing import Any, Callable, Iterable, Union


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


@dataclasses.dataclass
class FailResult:
    test_name: str
    _: dataclasses.KW_ONLY
    messages: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ErrorResult:
    test_name: str
    _: dataclasses.KW_ONLY
    error: Exception

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.test_name == other.test_name and self.error.args == other.error.args


def run_tests(tests: Iterable[TestFunction]) -> list[Union[PassResult, FailResult, ErrorResult]]:
    """
    Runs some tests functions and returns the result of each test.

    Test functions are ones which accept a single TestContext argument. The
    TestContext is used to make assertions and signal test failures. Tests
    which do not fail any assertions, call fail on the TestContext, or raise an
    exception are deemed to have passed.
    """
    results: list[Union[PassResult, FailResult, ErrorResult]] = []
    for test in tests:
        t = TestContext()
        try:
            test(t)
        except StopTest:
            pass
        except Exception as e:
            results.append(ErrorResult(test.__name__, error=e))
            continue
        if t._passed:
            results.append(PassResult(test.__name__))
        else:
            results.append(FailResult(test.__name__, messages=t._messages))
    return results
