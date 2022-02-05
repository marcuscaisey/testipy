from test_data.e2e.numbers import add
from testipy import TestContext


def test_passes(t: TestContext):
    x, y = 2, 3
    expected = 5
    actual = add(x, y)
    if not expected == actual:
        t.fail(f"expected {x} + {y} to be {expected}, got {actual}")
