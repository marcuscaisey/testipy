import unittest

from testipy import TestContext, run_test


class TestRunTest(unittest.TestCase):
    def test_test_passes_if_fail_not_called_on_context(self):
        def test_passes(t: TestContext):
            pass

        result = run_test(test_passes)

        self.assertTrue(result.is_pass, "expected test to pass")
        self.assertEqual("", result.message, "expected failure message to be empty")

    def test_test_fails_if_fail_called_on_context(self):
        def test_fails(t: TestContext):
            t.fail()

        result = run_test(test_fails)

        self.assertFalse(result.is_pass, "expected test to fail")
        self.assertEqual("", result.message, "expected failure message to be empty")

    def test_failure_message_is_saved_on_test_result(self):
        expected_message = "failure message"

        def test_fails(t: TestContext):
            t.fail(expected_message)

        result = run_test(test_fails)

        self.assertFalse(result.is_pass, "expected test to fail")
        self.assertEqual(
            "failure message",
            result.message,
            f"expected failure message to be {expected_message}, got {result.message}",
        )
