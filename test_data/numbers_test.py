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
    if not expected == actual:
        t.fail(f"expected {x} - {y} to be {expected}, got {actual}")


def test_multiple_failures(t: TestContext):
    t.fail("failure message 1")
    t.fail()
    t.fail("failure message 2")
