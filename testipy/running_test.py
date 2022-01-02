import unittest

from .running import TestContext, TestResult, run_tests


class TestRunTest(unittest.TestCase):
    longMessage = False

    def test_result_is_pass_when_fail_not_called_on_context(self):
        def test_passes(t: TestContext):
            pass

        actual = run_tests([test_passes])

        expected = [TestResult("test_passes", is_pass=True)]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected running a passing test to return {expected}, got {actual}",
        )

    def test_result_is_fail_when_fail_called_on_context(self):
        def test_fails(t: TestContext):
            t.fail()

        actual = run_tests([test_fails])

        expected = [TestResult("test_fails", is_pass=False)]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected running a failing test to return {expected}, got {actual}",
        )

    def test_can_call_fail_multiple_times(self):
        def test_fails(t: TestContext):
            t.fail()
            t.fail()

        actual = run_tests([test_fails])

        expected = [TestResult("test_fails", is_pass=False)]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected running a failing test to return {expected}, got {actual}",
        )

    def test_failure_message_is_set_on_result_when_fail_called_with_message(self):
        failure_message = "failure message"

        def test_fails(t: TestContext):
            t.fail(failure_message)

        actual = run_tests([test_fails])

        expected = [TestResult("test_fails", is_pass=False, messages=[failure_message])]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected failing a test with message: '{failure_message}' to return {expected}, got {actual}",
        )

    def test_multiple_messages_are_set_on_result_when_fail_called_multiple_times_with_message(self):
        failure_message_1 = "failure message 1"
        failure_message_2 = "failure message 2"

        def test_fails(t: TestContext):
            t.fail(failure_message_1)
            t.fail()
            t.fail(failure_message_2)

        actual = run_tests([test_fails])

        expected = [
            TestResult(
                "test_fails",
                is_pass=False,
                messages=[
                    failure_message_1,
                    failure_message_2,
                ],
            )
        ]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected failing a test with messages: '{failure_message_1}', '{failure_message_2}' to return {expected}, got {actual}",
        )

    def test_calling_fail_with_require_ends_test_right_away(self):
        def test_fails(t: TestContext):
            t.fail("failure message", require=True)
            t.fail("won't reach here")

        actual = run_tests([test_fails])

        expected = [TestResult("test_fails", is_pass=False, messages=["failure message"])]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected failing a test with require to return {expected}, got {actual}",
        )

    def test_result_is_error_when_exception_raised_inside_test(self):
        def test_errors(t: TestContext):
            raise ValueError("oh no!")

        actual = run_tests([test_errors])

        expected = [TestResult("test_errors", is_pass=False, error=ValueError("oh no!"))]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected erroring a test to return {expected}, got {actual}",
        )

    def test_running_multiple_tests_returns_a_result_for_each_test(self):
        def test_passes_1(t: TestContext):
            pass

        def test_passes_2(t: TestContext):
            pass

        actual = run_tests([test_passes_1, test_passes_2])

        expected = [
            TestResult("test_passes_1", is_pass=True),
            TestResult("test_passes_2", is_pass=True),
        ]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected running multiple tests together to return {expected}, got {actual}",
        )

    def test_exception_raised_in_test_doesnt_affect_other_tests(self):
        def test_fails(t: TestContext):
            t.fail()

        def test_errors(t: TestContext):
            raise ValueError("oh no!")

        def test_passes(t: TestContext):
            pass

        actual = run_tests([test_fails, test_errors, test_passes])

        expected = [
            TestResult("test_fails", is_pass=False),
            TestResult("test_errors", is_pass=False, error=ValueError("oh no!")),
            TestResult("test_passes", is_pass=True),
        ]
        self.assertResultsEqual(
            expected,
            actual,
            f"expected running mix of passing / failing / erroring tests to return {expected}, got {actual}",
        )

    def assertResultsEqual(
        self, expected: list[TestResult], actual: list[TestResult], message: str
    ):
        self.assertEqual(len(expected), len(actual), message)
        for expected_result, actual_result in zip(expected, actual):
            if not test_results_equal(expected_result, actual_result):
                self.fail(message)


def test_results_equal(r1: TestResult, r2: TestResult) -> bool:
    if not (
        r1.test_name == r2.test_name and r1.is_pass == r2.is_pass and r1.messages == r2.messages
    ):
        return False
    if r1.error is None or r2.error is None:
        return r1.error is None and r2.error is None
    return type(r1.error) is type(r2.error) and r1.error.args == r2.error.args
