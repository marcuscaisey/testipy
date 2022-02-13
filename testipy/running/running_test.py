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
    longMessage = False

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

    def test_invalid_test_methods_are_skipped(self):
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

    def test_test_methods_state_is_isolated_from_each_other(self):
        class TestClass:
            def test_sets_x(self, t: TestContext):
                self.x = 2

            def test_checks_for_x(self, t: TestContext):
                # test_sets_x set x = 2 but that state should be isolated from this test
                t.assert_false(hasattr(self, "x"))

        actual = run_tests([TestClass])

        expected = [
            PassResult(
                "TestClass",
                sub_results=[PassResult("test_sets_x"), PassResult("test_checks_for_x")],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with passing tests to return {expected}, got {actual}",
        )


class TestSetup(unittest.TestCase):
    longMessage = False

    def test_setup_is_run_before_each_test_method(self):
        methods_called = []

        class TestSetup:
            def setup(self):
                methods_called.append("setup")

            def test_first(self, t: TestContext):
                methods_called.append("test_first")

            def test_second(self, t: TestContext):
                methods_called.append("test_second")

        actual_results = run_tests([TestSetup])

        expected_results = [
            PassResult(
                "TestSetup",
                sub_results=[PassResult("test_first"), PassResult("test_second")],
            )
        ]
        self.assertEqual(
            expected_results,
            actual_results,
            f"expected running class with setup method to return {expected_results}, got {actual_results}",
        )
        expected_methods_called = ["setup", "test_first", "setup", "test_second"]
        self.assertEqual(
            expected_methods_called,
            methods_called,
            f"expected running class with setup method to call methods in order {expected_methods_called}, got {methods_called}",
        )

    def test_variables_can_be_shared_between_setup_and_test_method(self):
        class TestSetup:
            def setup(self):
                self.x = 2

            def test_first(self, t: TestContext):
                # setup should have set x = 2
                t.assert_equal(2, self.x)

            def test_second(self, t: TestContext):
                # setup should have set x = 2
                t.assert_equal(2, self.x)

        actual = run_tests([TestSetup])

        expected = [
            PassResult(
                "TestSetup",
                sub_results=[PassResult("test_first"), PassResult("test_second")],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with setup method to return {expected}, got {actual}",
        )

    def test_result_is_error_if_exception_raised_in_setup(self):
        class TestFailsSetup:
            def setup(self):
                raise ValueError("oh no!")

            def test_wont_reach_this_test(self, t: TestContext):
                t.assert_equal(1, 2)

        actual = run_tests([TestFailsSetup])

        expected = [ErrorResult("TestFailsSetup", error=ValueError("oh no!"))]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with erroring setup method to return {expected}, got {actual}",
        )

    def test_error_result_contains_test_results_from_before_setup_error_if_setup_error_raised(self):
        run_count = 0

        class TestFailsSetup:
            def setup(self):
                """Raises an exception on the fourth run."""
                nonlocal run_count
                run_count += 1
                if run_count == 4:
                    raise ValueError("oh no in setup!")

            def test_passes(self, t: TestContext):
                t.assert_equal(1, 1)

            def test_fails(self, t: TestContext):
                t.assert_equal(1, 2)

            def test_errors(self, t: TestContext):
                raise ValueError("oh no!")

            def test_wont_reach_this_test(self, t: TestContext):
                pass

        actual = run_tests([TestFailsSetup])

        expected = [
            ErrorResult(
                "TestFailsSetup",
                error=ValueError("oh no in setup!"),
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["Expected 1 and 2 to be equal"]),
                    ErrorResult("test_errors", error=ValueError("oh no!")),
                ],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with erroring setup method to return {expected}, got {actual}",
        )

    def test_setup_is_isolated_from_any_state_set_in_previous_test_methods(self):
        class TestSetup:
            def setup(self):
                # test_sets_x set x = 3 but setup should be isolated from that state change so won't
                # see it
                if hasattr(self, "x"):
                    self.can_see_x = True
                else:
                    self.can_see_x = False

            def test_sets_x(self, t: TestContext):
                t.assert_equal(1, 1)
                self.x = 3

            def test_checks_for_x(self, t: TestContext):
                t.assert_false(self.can_see_x)

        actual = run_tests([TestSetup])

        expected = [
            PassResult(
                "TestSetup",
                sub_results=[PassResult("test_sets_x"), PassResult("test_checks_for_x")],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with setup method to return {expected}, got {actual}",
        )


class TestSetupClass(unittest.TestCase):
    longMessage = False

    def test_setup_class_is_run_before_all_test_methods(self):
        methods_called = []

        class TestSetupClass:
            @classmethod
            def setup_class(cls):
                methods_called.append("setup_class")

            def test_first(self, t: TestContext):
                methods_called.append("test_first")

            def test_second(self, t: TestContext):
                methods_called.append("test_second")

        actual_results = run_tests([TestSetupClass])

        expected_results = [
            PassResult(
                "TestSetupClass",
                sub_results=[PassResult("test_first"), PassResult("test_second")],
            )
        ]
        self.assertEqual(
            expected_results,
            actual_results,
            f"expected running class with setup_class method to return {expected_results}, got {actual_results}",
        )
        expected_methods_called = ["setup_class", "test_first", "test_second"]
        self.assertEqual(
            expected_methods_called,
            methods_called,
            f"expected running class with setup_class method to call methods in order {expected_methods_called}, got {methods_called}",
        )

    def test_variables_can_be_shared_between_setup_class_and_test_methods(self):
        class TestSetupClass:
            @classmethod
            def setup_class(cls):
                cls.x = 1

            def test_first(self, t: TestContext):
                # setup_class should have set x = 1
                t.assert_equal(1, self.x)

            def test_second(self, t: TestContext):
                # x should still be 1 from setup_class
                t.assert_equal(1, self.x)

        actual = run_tests([TestSetupClass])

        expected = [
            PassResult(
                "TestSetupClass",
                sub_results=[PassResult("test_first"), PassResult("test_second")],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with setup_class method to return {expected}, got {actual}",
        )

    def test_result_is_error_if_exception_raised_in_setup_class(self):
        class TestFailsSetupClass:
            @classmethod
            def setup_class(self):
                raise ValueError("oh no!")

            def test_wont_reach_this_test(self, t: TestContext):
                t.assert_equal(1, 2)

        actual = run_tests([TestFailsSetupClass])

        expected = [ErrorResult("TestFailsSetupClass", error=ValueError("oh no!"))]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with erroring setup_class method to return {expected}, got {actual}",
        )


class TestTeardown(unittest.TestCase):
    longMessage = False

    def test_teardown_is_run_after_each_method(self):
        methods_called = []

        class TestTeardown:
            def teardown(self):
                methods_called.append("teardown")

            def test_first(self, t: TestContext):
                methods_called.append("test_first")

            def test_second(self, t: TestContext):
                methods_called.append("test_second")

        actual_results = run_tests([TestTeardown])

        expected_results = [
            PassResult(
                "TestTeardown",
                sub_results=[PassResult("test_first"), PassResult("test_second")],
            )
        ]
        self.assertEqual(
            expected_results,
            actual_results,
            f"expected running class with teardown method to return {expected_results}, got {actual_results}",
        )
        expected_methods_called = ["test_first", "teardown", "test_second", "teardown"]
        self.assertEqual(
            expected_methods_called,
            methods_called,
            f"expected running class with teardown method to call methods in order {expected_methods_called}, got {methods_called}",
        )

    def test_error_result_contains_test_results_from_before_teardown_error_if_teardown_error_raised(
        self,
    ):
        run_count = 0

        class TestFailsTeardown:
            def teardown(self):
                """Raises an exception on the third run."""
                nonlocal run_count
                run_count += 1
                if run_count == 3:
                    raise ValueError("oh no in teardown!")

            def test_passes(self, t: TestContext):
                t.assert_equal(1, 1)

            def test_fails(self, t: TestContext):
                t.assert_equal(1, 2)

            def test_errors(self, t: TestContext):
                raise ValueError("oh no!")

            def test_wont_reach_this(self, t: TestContext):
                pass

        actual = run_tests([TestFailsTeardown])

        expected = [
            ErrorResult(
                "TestFailsTeardown",
                error=ValueError("oh no in teardown!"),
                sub_results=[
                    PassResult("test_passes"),
                    FailResult("test_fails", messages=["Expected 1 and 2 to be equal"]),
                    ErrorResult("test_errors", error=ValueError("oh no!")),
                ],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with erroring teardown method to return {expected}, got {actual}",
        )

    def test_tests_are_isolated_from_any_state_set_in_teardown_method(self):
        class TestTeardown:
            def teardown(self):
                self.x = 2

            def test_passes(self, t: TestContext):
                t.assert_equal(1, 1)

            def test_cant_see_x(self, t: TestContext):
                # teardown set x = 2 but this test should be isolated from that state change
                t.assert_false(hasattr(self, "x"))

        actual = run_tests([TestTeardown])

        expected = [
            PassResult(
                "TestTeardown",
                sub_results=[PassResult("test_passes"), PassResult("test_cant_see_x")],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with teardown method to return {expected}, got {actual}",
        )


class TestTeardownClass(unittest.TestCase):
    longMessage = False

    def test_teardown_class_is_run_once_after_all_test_methods(self):
        methods_called = []

        class TestTeardownClass:
            @classmethod
            def teardown_class(cls):
                methods_called.append("teardown_class")

            def test_first(self, t: TestContext):
                methods_called.append("test_first")

            def test_second(self, t: TestContext):
                methods_called.append("test_second")

        actual_results = run_tests([TestTeardownClass])

        expected_results = [
            PassResult(
                "TestTeardownClass",
                sub_results=[PassResult("test_first"), PassResult("test_second")],
            )
        ]
        self.assertEqual(
            expected_results,
            actual_results,
            f"expected running class with teardown_class method to return {expected_results}, got {actual_results}",
        )
        expected_methods_called = ["test_first", "test_second", "teardown_class"]
        self.assertEqual(
            expected_methods_called,
            methods_called,
            f"expected running class with teardown_class method to call methods in order {expected_methods_called}, got {methods_called}",
        )

    def test_result_is_error_if_exception_raised_in_teardown_class(self):
        class TestFailsTeardownClass:
            @classmethod
            def teardown_class(self):
                raise ValueError("oh no!")

            def test_passes(self, t: TestContext):
                t.assert_equal(1, 1)

        actual = run_tests([TestFailsTeardownClass])

        expected = [
            ErrorResult(
                "TestFailsTeardownClass",
                error=ValueError("oh no!"),
                sub_results=[PassResult("test_passes")],
            )
        ]
        self.assertEqual(
            expected,
            actual,
            f"expected running class with erroring teardown_class method to return {expected}, got {actual}",
        )
