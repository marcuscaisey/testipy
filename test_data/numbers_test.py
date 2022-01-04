from testipy import TestContext

from test_data.numbers import add, sub


def test_add(t: TestContext):
    x, y = 2, 3
    expected = 5
    actual = add(x, y)
    if not expected == actual:
        t.fail(f"expected {x} + {y} to be {expected}, got {actual}")


def test_sub(t: TestContext):
    x, y = 2, 3
    expected = -1
    actual = sub(x, y)
    t.assert_equal(expected, actual, "this is most disappointing")


def test_multiple_failures(t: TestContext):
    t.fail("failure message")
    t.fail()
    t.fail("multiple failures are allowed in the same test")


def raises_exception():
    raise ValueError("oh no!")


def test_exceptions_error_the_test(t: TestContext):
    raises_exception()


def test_require_failure(t: TestContext):
    t.fail("requiring a failure stops the test", require=True)
    t.fail("won't reach here")
