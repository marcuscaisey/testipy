import unittest

from .running import ErrorResult, FailResult, PassResult, TestContext, run_tests


class TestRunTests(unittest.TestCase):
    longMessage = False

    def test_result_is_pass_when_fail_not_called_on_context(self):
        def test_passes(t: TestContext):
            pass

        actual = run_tests([test_passes])

        expected = [PassResult("test_passes")]
        self.assertEqual(
            expected,
            actual,
            f"expected running a passing test to return {expected}, got {actual}",
        )

    def test_result_is_fail_when_fail_called_on_context(self):
        def test_fails(t: TestContext):
            t.fail()

        actual = run_tests([test_fails])

        expected = [FailResult("test_fails")]
        self.assertEqual(
            expected,
            actual,
            f"expected running a failing test to return {expected}, got {actual}",
        )

    def test_can_call_fail_multiple_times(self):
        def test_fails(t: TestContext):
            t.fail()
            t.fail()

        actual = run_tests([test_fails])

        expected = [FailResult("test_fails")]
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

        expected = [FailResult("test_fails", messages=[failure_message])]
        self.assertEqual(
            expected,
            actual,
            f"expected failing a test with message: '{failure_message}' to return {expected}, got {actual}",
        )

    def test_multiple_messages_are_set_on_result_when_fail_called_multiple_times_with_message(
        self,
    ):
        failure_message_1 = "failure message 1"
        failure_message_2 = "failure message 2"

        def test_fails(t: TestContext):
            t.fail(failure_message_1)
            t.fail()
            t.fail(failure_message_2)

        actual = run_tests([test_fails])

        expected = [FailResult("test_fails", messages=[failure_message_1, failure_message_2])]
        self.assertEqual(
            expected,
            actual,
            f"expected failing a test with messages: '{failure_message_1}', '{failure_message_2}' to return {expected}, got {actual}",
        )

    def test_calling_fail_with_require_ends_test_right_away(self):
        def test_fails(t: TestContext):
            t.fail("failure message", require=True)
            t.fail("won't reach here")

        actual = run_tests([test_fails])

        expected = [FailResult("test_fails", messages=["failure message"])]
        self.assertEqual(
            expected,
            actual,
            f"expected failing a test with require to return {expected}, got {actual}",
        )

    def test_result_is_error_when_exception_raised_inside_test(self):
        def test_errors(t: TestContext):
            raise ValueError("oh no!")

        actual = run_tests([test_errors])

        expected = [ErrorResult("test_errors", error=ValueError("oh no!"))]
        self.assertEqual(
            expected,
            actual,
            f"expected erroring a test to return {expected}, got {actual}",
        )

    def test_running_multiple_tests_returns_multiple_results_in_same_order(self):
        def test_passes_2(t: TestContext):
            pass

        def test_passes_1(t: TestContext):
            pass

        actual = run_tests([test_passes_1, test_passes_2])

        expected = [PassResult("test_passes_1"), PassResult("test_passes_2")]

        self.assertEqual(
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
            FailResult("test_fails"),
            ErrorResult("test_errors", error=ValueError("oh no!")),
            PassResult("test_passes"),
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running mix of passing / failing / erroring tests to return {expected}, got {actual}",
        )


class TestAssertEqual(unittest.TestCase):
    longMessage = False

    def test_test_passes_if_objects_are_equal(self):
        def test_passes(t: TestContext):
            t.assert_equal(2, 2)

        actual = run_tests([test_passes])

        expected = [PassResult("test_passes")]
        self.assertEqual(
            expected,
            actual,
            f"expected test to pass when asserting that two equal objects are equal, got {actual}",
        )

    def test_test_fails_with_default_message_if_objects_are_not_equal(self):
        def test_fails(t: TestContext):
            t.assert_equal(2, 3)

        actual = run_tests([test_fails])

        expected = [FailResult("test_fails", messages=["Expected 2 and 3 to be equal"])]
        self.assertEqual(
            expected,
            actual,
            f"expected test to fail when asserting that two unequal objects are equal, got {actual}",
        )

    def test_test_fails_with_custom_message_if_given(self):
        def test_fails(t: TestContext):
            t.assert_equal(2, 3, "this is most disappointing")

        actual = run_tests([test_fails])

        expected = [
            FailResult(
                "test_fails", messages=["Expected 2 and 3 to be equal; this is most disappointing"]
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected test to fail with custom failure message, got {actual}",
        )

    def test_calling_with_require_ends_test_right_away(self):
        def test_fails(t: TestContext):
            t.assert_equal(2, 3, require=True)
            t.fail("won't reach here")

        actual = run_tests([test_fails])

        expected = [FailResult("test_fails", messages=["Expected 2 and 3 to be equal"])]
        self.assertEqual(
            expected,
            actual,
            f"expected asserting with require to return {expected}, got {actual}",
        )
