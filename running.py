"""
Defines run_tests which is the way that tests should be run. It returns a list
of test results which can then be given to a formatter.
"""
import dataclasses
from typing import Callable, Iterable


@dataclasses.dataclass(order=False)
class TestResult:
    """Object which contains information about a test run."""

    test_name: str
    is_pass: bool = True
    message: str = ""

    def _fail(self, message: str):
        """Fail the current test."""
        self.is_pass = False
        self.message = message


class TestContext:
    """Object made available inside tests to manage test state."""

    def __init__(self, test_name: str):
        """
        Args:
            test_name: The name of the test that this context is being used by
        """
        self.result = TestResult(test_name)

    def fail(self, message: str = ""):
        """Fail the current test, optionally with a given failure message."""
        self.result._fail(message)


TestFunction = Callable[[TestContext], None]


def run_tests(tests: Iterable[TestFunction]) -> list[TestResult]:
    """
    Runs some tests functions and returns the result of each test.

    Test functions are ones which accept a single TestContext argument. The
    TestContext is used to make assertions and signal test failures. Tests
    which do not fail any assertions, call fail on the TestContext, or raise an
    exception are deemed to have passed.
    """
    results = []
    for test in tests:
        t = TestContext(test.__name__)
        test(t)
        results.append(t.result)
    return results
