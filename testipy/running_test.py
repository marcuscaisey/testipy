import unittest

from .running import TestContext, TestResult, run_tests


class TestRunTest(unittest.TestCase):
    longMessage = False

    def test_result_is_pass_when_fail_not_called_on_context(self):
        def test_passes(t: TestContext):
            pass

        actual = run_tests([test_passes])

        expected = [TestResult("test_passes", is_pass=True)]
        self.assertEqual(
            expected,
            actual,
            f"expected running a passing test to return {expected}, got {actual}",
        )

    def test_result_is_fail_when_fail_called_on_context(self):
        def test_fails(t: TestContext):
            t.fail()

        actual = run_tests([test_fails])

        expected = [TestResult("test_fails", is_pass=False)]
        self.assertEqual(
            expected,
            actual,
            f"expected running a failing test to return {expected}, got {actual}",
        )

    def test_failure_message_is_set_on_result_when_fail_called_with_message(self):
        failure_message = "failure message"

        def test_fails(t: TestContext):
            t.fail(failure_message)

        actual = run_tests([test_fails])

        expected = [TestResult("test_fails", is_pass=False, message=failure_message)]
        self.assertEqual(
            expected,
            actual,
            f"expected failing a test with message: '{failure_message}' to return {expected}, got {actual}",
        )

    def test_running_multiple_tests_returns_a_result_for_each_test(self):
        def test_passes(t: TestContext):
            pass

        def test_fails(t: TestContext):
            t.fail()

        actual = run_tests([test_passes, test_fails])

        expected = [
            TestResult("test_passes", is_pass=True),
            TestResult("test_fails", is_pass=False),
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running multiple tests together to return {expected}, got {actual}",
        )
