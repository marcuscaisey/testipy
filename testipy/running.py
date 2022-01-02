from typing import Callable, Iterable


class StopTest(Exception):
    """Raised to signal that the current test should be stopped."""

    pass


class TestResult:
    """Object which contains information about a test run."""

    def __init__(
        self,
        test_name: str,
        *,
        is_pass: bool = True,
        messages: list[str] = None,
        error: Exception = None,
    ):
        self.test_name = test_name
        self.is_pass = is_pass
        self.messages = messages or []
        self.error = error

    def _fail(self, message: str = ""):
        """Fail the current test."""
        self.is_pass = False
        if message:
            self.messages.append(message)

    def __repr__(self) -> str:
        args = [
            repr(self.test_name),
            f"is_pass={self.is_pass}",
        ]
        if self.messages:
            args.append(f"messages={self.messages!r}")
        if self.error:
            args.append(f"error={self.error!r}")
        return f"TestResult({', '.join(args)})"


class TestContext:
    """Object made available inside tests to manage test state."""

    def __init__(self, test_name: str):
        """
        Args:
            test_name: The name of the test that this context is being used by
        """
        self._result = TestResult(test_name)

    def fail(self, message: str = "", *, require=False):
        """Fail the current test, optionally with a given failure message."""
        self._result._fail(message)
        if require:
            raise StopTest()


TestFunction = Callable[[TestContext], None]


def run_tests(tests: Iterable[TestFunction]) -> list[TestResult]:
    """
    Runs some tests functions and returns the result of each test.

    Test functions are ones which accept a single TestContext argument. The
    TestContext is used to make assertions and signal test failures. Tests
    which do not fail any assertions, call fail on the TestContext, or raise an
    exception are deemed to have passed.
    """
    results = [_run_test(test) for test in tests]
    return results


def _run_test(test: TestFunction) -> TestResult:
    t = TestContext(test.__name__)
    try:
        test(t)
    except StopTest:
        pass
    except Exception as e:
        t._result._fail()
        t._result.error = e
    return t._result
