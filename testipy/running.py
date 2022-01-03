import dataclasses
from typing import Any, Callable, Iterable


class StopTest(Exception):
    """Raised to signal that the current test should be stopped."""

    pass


@dataclasses.dataclass
class TestResult:
    """
    The result of a test run.

    Attributes:
        test_order: The order that this test ran in. Starts from 1.
        test_name: The name of the test that ran
    """

    test_order: int
    test_name: str


@dataclasses.dataclass
class PassResult(TestResult):
    """
    The result of a passing test.

    Attributes:
        test_order: The order that this test ran in. Starts from 1.
        test_name: The name of the test that ran
    """

    pass


@dataclasses.dataclass
class FailResult(TestResult):
    """
    The result of a failing test.

    Attributes:
        test_order: The order that the test ran in. Starts from 1.
        test_name: The name of the test that ran
        messages: The failure messages added during the test run
    """

    _: dataclasses.KW_ONLY
    messages: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ErrorResult(TestResult):
    """
    The result of an errored test.

    Attributes:
        test_order: The order that the test ran in. Starts from 1.
        test_name: The name of the test that ran
        error: The exception that was raised during the test run
    """

    error: Exception

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.test_order == other.test_order
            and self.test_name == other.test_name
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


class TestContext:
    """Object made available inside tests to manage test state."""

    def __init__(self):
        self._passed = True
        self._messages = []

    def fail(self, message: str = "", *, require=False):
        """Fail the current test, optionally with a given failure message."""
        self._passed = False
        if message:
            self._messages.append(message)
        if require:
            raise StopTest()


TestFunction = Callable[[TestContext], None]


def run_tests(tests: Iterable[TestFunction]) -> TestResults:
    """
    Runs some tests functions and returns the result of each test.

    Test functions are ones which accept a single TestContext argument. The
    TestContext is used to make assertions and signal test failures. Tests
    which do not fail any assertions, call fail on the TestContext, or raise an
    exception are deemed to have passed.
    """
    results = TestResults()
    for i, test in enumerate(tests, 1):
        t = TestContext()
        try:
            test(t)
        except StopTest:
            pass
        except Exception as e:
            result = ErrorResult(i, test.__name__, e)
            results.errored.append(result)
            continue
        if t._passed:
            result = PassResult(i, test.__name__)
            results.passed.append(result)
        else:
            result = FailResult(i, test.__name__, messages=t._messages)
            results.failed.append(result)
    return results
