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
        test: The test that ran.
    """

    test: TestFunction


@dataclasses.dataclass
class FailResult:
    """
    The result of a failing test.

    Attributes:
        test: The test that ran.
        messages: The failure messages added during the test run.
    """

    test: TestFunction
    _: dataclasses.KW_ONLY
    messages: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ErrorResult:
    """
    The result of an errored test.

    Attributes:
        test: The test that ran.
        error: The exception that was raised during the test run
    """

    test: TestFunction
    error: Exception

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.test is other.test
            and type(self.error) is type(other.error)
            and self.error.args == other.error.args
        )


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
    for test in tests:
        t = TestContext()
        try:
            test(t)
        except StopTest:
            pass
        except Exception as e:
            results.errored.append(ErrorResult(test, e))
            continue
        if t._passed:
            results.passed.append(PassResult(test))
        else:
            results.failed.append(FailResult(test, messages=t._messages))
    return results
