from testipy import TestContext

from test_data.e2e.numbers import add


class TestAdd:
    def test_adding_two_and_three_returns_five(self, t: TestContext):
        actual = add(2, 3)
        expected = 5
        t.assert_equal(expected, actual, "this is most disappointing")

    def test_adding_three_and_three_returns_seven(self, t: TestContext):
        actual = add(3, 3)
        expected = 7
        t.assert_equal(expected, actual, "this is most disappointing")
