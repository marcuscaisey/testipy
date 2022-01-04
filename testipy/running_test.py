import unittest

from .running import ErrorResult, FailResult, PassResult, TestContext, TestResults, run_tests


class TestRunTests(unittest.TestCase):
    longMessage = False

    def test_result_is_pass_when_fail_not_called_on_context(self):
        def test_passes(t: TestContext):
            pass

        actual = run_tests([test_passes])

        expected = TestResults(passed=[PassResult(test_passes)])
        self.assertEqual(
            expected,
            actual,
            f"expected running a passing test to return {expected}, got {actual}",
        )

    def test_result_is_fail_when_fail_called_on_context(self):
        def test_fails(t: TestContext):
            t.fail()

        actual = run_tests([test_fails])

        expected = TestResults(failed=[FailResult(test_fails)])
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

        expected = TestResults(failed=[FailResult(test_fails)])
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

        expected = TestResults(failed=[FailResult(test_fails, messages=[failure_message])])
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

        expected = TestResults(
            failed=[FailResult(test_fails, messages=[failure_message_1, failure_message_2])]
        )
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

        expected = TestResults(failed=[FailResult(test_fails, messages=["failure message"])])
        self.assertEqual(
            expected,
            actual,
            f"expected failing a test with require to return {expected}, got {actual}",
        )

    def test_result_is_error_when_exception_raised_inside_test(self):
        def test_errors(t: TestContext):
            raise ValueError("oh no!")

        actual = run_tests([test_errors])

        expected = TestResults(errored=[ErrorResult(test_errors, ValueError("oh no!"))])
        self.assertEqual(
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

        expected = TestResults(passed=[PassResult(test_passes_1), PassResult(test_passes_2)])
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

        expected = TestResults(
            passed=[PassResult(test_passes)],
            failed=[FailResult(test_fails)],
            errored=[ErrorResult(test_errors, ValueError("oh no!"))],
        )
        self.assertEqual(
            expected,
            actual,
            f"expected running mix of passing / failing / erroring tests to return {expected}, got {actual}",
        )


# class TestTestResults(unittest.TestCase):
#     longMessage = False

#     def test_equal_returns_true_between_equal_results(self):
#         results = TestResults(
#             passed=[PassResult(1, "test_passes_1")],
#             failed=[FailResult(2, "test_fails")],
#             errored=[ErrorResult(3, "test_errors", ValueError("oh no"))],
#         )

#         self.assertEqual(results, results, f"expected {results} to be equal to itself")

#     def test_equal_returns_false_when_comparing_against_other_types(self):
#         results = TestResults(
#             passed=[PassResult(1, "test_passes_1")],
#             failed=[FailResult(2, "test_fails")],
#             errored=[ErrorResult(3, "test_errors", ValueError("oh no"))],
#         )
#         other = [1, 2, 3]

#         self.assertNotEqual(results, other, f"expected {results} to not equal {other}")
