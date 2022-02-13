from typing import Any


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

    def assert_true(self, value: Any, message: str = "", require: bool = False):
        """Assert that value is True, failing the test if not."""
        if value is True:
            return
        failure_message = f"Expected {repr(value)} to be True"
        if message:
            failure_message += f"; {message}"
        self.fail(failure_message, require=require)

    def assert_false(self, value: Any, message: str = "", require: bool = False):
        """Assert that value is False, failing the test if not."""
        if value is False:
            return
        failure_message = f"Expected {repr(value)} to be False"
        if message:
            failure_message += f"; {message}"
        self.fail(failure_message, require=require)
