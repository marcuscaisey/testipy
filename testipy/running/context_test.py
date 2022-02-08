import unittest

from .context import TestContext
from .results import PassResult, FailResult
from .running import run_tests


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
