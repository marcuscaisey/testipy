from test_data.e2e.numbers import sub
from testipy import TestContext


def test_assert_equal(t: TestContext):
    x, y = 2, 3
    expected = -1
    actual = sub(x, y)
    t.assert_equal(expected, actual, "this is most disappointing")
