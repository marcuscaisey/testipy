import unittest

from .running import ErrorResult, FailResult, PassResult, TestContext, run_tests


class TestFunctionBasedTests(unittest.TestCase):
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
            f"expected failing a test with message: '{failure_message}' to return {expected}, "
            f"got {actual}",
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
            f"expected failing a test with messages: '{failure_message_1}', '{failure_message_2}' "
            f"to return {expected}, got {actual}",
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

    def test_running_multiple_tests_returns_multiple_results(self):
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
            f"expected running mix of passing / failing / erroring tests to return {expected}, "
            f"got {actual}",
        )


class TestClassBasedTests(unittest.TestCase):
    longMessage = None

    def test_result_is_pass_with_pass_sub_result_when_fail_not_called_on_context(self):
        class TestPasses:
            def test_passes(self, t: TestContext):
                pass

        actual = run_tests([TestPasses])

        expected = [PassResult("TestPasses", sub_results=[PassResult("test_passes")])]
        self.assertEqual(
            expected,
            actual,
            f"expected running a class with a passing test to return {expected}, got {actual}",
        )

    def test_result_is_fail_with_fail_sub_result_when_fail_called_on_context(self):
        class TestFails:
            def test_fails(self, t: TestContext):
                t.fail()

        actual = run_tests([TestFails])

        expected = [FailResult("TestFails", sub_results=[FailResult("test_fails")])]
        self.assertEqual(
            expected,
            actual,
            f"expected running a class with a failing test to return {expected}, got {actual}",
        )

    def test_can_call_fail_multiple_times(self):
        class TestFails:
            def test_fails(self, t: TestContext):
                t.fail()
                t.fail()

        actual = run_tests([TestFails])

        expected = [FailResult("TestFails", sub_results=[FailResult("test_fails")])]
        self.assertEqual(
            expected,
            actual,
            f"expected running a class with a failing test to return {expected}, got {actual}",
        )

    def test_failure_message_is_set_on_sub_result_when_fail_called_with_message(self):
        failure_message = "failure message"

        class TestFails:
            def test_fails(self, t: TestContext):
                t.fail(failure_message)

        actual = run_tests([TestFails])

        expected = [
            FailResult(
                "TestFails",
                sub_results=[FailResult("test_fails", messages=[failure_message])],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected failing a test in a test class with message: '{failure_message}' to return "
            f"{expected}, got {actual}",
        )

    def test_multiple_messages_are_set_on_sub_result_when_fail_called_multiple_times_with_message(
        self,
    ):
        failure_message_1 = "failure message 1"
        failure_message_2 = "failure message 2"

        class TestFails:
            def test_fails(self, t: TestContext):
                t.fail(failure_message_1)
                t.fail()
                t.fail(failure_message_2)

        actual = run_tests([TestFails])

        expected = [
            FailResult(
                "TestFails",
                sub_results=[
                    FailResult("test_fails", messages=[failure_message_1, failure_message_2])
                ],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected failing a test in a class with messages: '{failure_message_1}', "
            f"'{failure_message_2}' to return {expected}, got {actual}",
        )

    def test_result_is_pass_with_pass_sub_results_when_all_tests_pass(self):
        class TestPasses:
            def test_passes_1(self, t: TestContext):
                pass

            def test_passes_2(self, t: TestContext):
                pass

        actual = run_tests([TestPasses])

        expected = [
            PassResult(
                "TestPasses",
                sub_results=[PassResult("test_passes_1"), PassResult("test_passes_2")],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running a class with multiple passing tests to return {expected}, "
            f"got {actual}",
        )

    def test_sub_results_are_in_same_order_as_tests(self):
        class TestPasses:
            def test_b(self, t: TestContext):
                pass

            def test_a(self, t: TestContext):
                pass

        actual = run_tests([TestPasses])

        expected = [
            PassResult("TestPasses", sub_results=[PassResult("test_b"), PassResult("test_a")])
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running a class with multiple tests to return {expected}, got {actual}",
        )

    def test_result_is_fail_when_some_tests_fail(self):
        class TestFails:
            def test_passes(self, t: TestContext):
                pass

            def test_fails(self, t: TestContext):
                t.fail("oh no!")

        actual = run_tests([TestFails])

        expected = [
            FailResult(
                "TestFails",
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["oh no!"]),
                ],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running a class with a passing and a failing test to return {expected}, "
            f"got {actual}",
        )

    def test_running_multiple_classes_returns_multiple_results_with_sub_results(self):
        class TestPasses:
            def test_passes_1(self, t: TestContext):
                pass

            def test_passes_2(self, t: TestContext):
                pass

        class TestFails:
            def test_passes(self, t: TestContext):
                pass

            def test_fails(self, t: TestContext):
                t.fail("oh no!")

        actual = run_tests([TestPasses, TestFails])

        expected = [
            PassResult(
                "TestPasses",
                sub_results=[PassResult("test_passes_1"), PassResult("test_passes_2")],
            ),
            FailResult(
                "TestFails",
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["oh no!"]),
                ],
            ),
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running multiple classes to return {expected}, got {actual}",
        )

    def test_calling_fail_with_require_ends_test_right_away(self):
        class TestFails:
            def test_fails(self, t: TestContext):
                t.fail("failure message", require=True)
                t.fail("won't reach here")

        actual = run_tests([TestFails])

        expected = [
            FailResult(
                "TestFails",
                sub_results=[FailResult("test_fails", messages=["failure message"])],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected failing a test in a class with require to return {expected}, got {actual}",
        )

    def test_result_is_error_with_error_sub_result_when_exception_raised_inside_test(self):
        class TestErrors:
            def test_errors(self, t: TestContext):
                raise ValueError("oh no!")

        actual = run_tests([TestErrors])

        expected = [
            ErrorResult(
                "TestErrors",
                sub_results=[ErrorResult("test_errors", error=ValueError("oh no!"))],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected erroring a test in a class to return {expected}, got {actual}",
        )

    def test_result_is_error_when_some_tests_error(self):
        class TestErrors:
            def test_errors(self, t: TestContext):
                raise ValueError("oh no!")

            def test_fails(self, t: TestContext):
                t.fail("oh no!")

            def test_passes(self, t: TestContext):
                pass

        actual = run_tests([TestErrors])

        expected = [
            ErrorResult(
                "TestErrors",
                sub_results=[
                    ErrorResult("test_errors", error=ValueError("oh no!")),
                    FailResult("test_fails", messages=["oh no!"]),
                    PassResult("test_passes"),
                ],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running a class with a passing / failing / erroring tests to return "
            f"{expected}, got {actual}",
        )

    def test_can_run_test_functions_and_test_classes_together(self):
        def test_passes(t: TestContext):
            t.assert_equal(1, 1)

        class TestFails:
            def test_passes(self, t: TestContext):
                t.assert_equal(2, 2)

            def test_fails(self, t: TestContext):
                t.assert_equal(3, 4)

        def test_fails(t: TestContext):
            t.assert_equal(4, 5)

        actual = run_tests([test_passes, TestFails, test_fails])

        expected = [
            PassResult("test_passes"),
            FailResult(
                "TestFails",
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["Expected 3 and 4 to be equal"]),
                ],
            ),
            FailResult("test_fails", messages=["Expected 4 and 5 to be equal"]),
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running test functions and tests classes together to return {expected}, "
            f"got {actual}",
        )

    def test_methods_(self):
        class TestFails:
            def foo(self):
                pass

            def test_missing_test_context(self):
                pass

            def test_fails(self, t: TestContext):
                t.assert_equal(3, 4)

            def test_untyped_test_context(self, t):
                t.fail("oh no!")

            def no_test_prefix(self, t: TestContext):
                t.fail("oh no!")

        actual = run_tests([TestFails])

        expected = [
            FailResult(
                "TestFails",
                sub_results=[
                    FailResult("test_fails", messages=["Expected 3 and 4 to be equal"]),
                ],
            ),
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with invalid test methods in to return {expected}, "
            f"got {actual}",
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
            f"expected test to fail when asserting that two unequal objects are equal, "
            f"got {actual}",
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
