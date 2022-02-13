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


counter = None


class TestSetupAndTeardown:
    torn_class_down = False

    @classmethod
    def setup_class(cls):
        global counter
        counter = 0
        cls.counter = counter

    def setup(self):
        global counter
        counter += 2
        self.counter += counter

    def teardown(self):
        global counter
        counter -= 1

    def test_first(self, t: TestContext):
        t.assert_false(self.torn_class_down)
        # setup_class: counter = 0
        # setup (test_first): counter = counter + 2 = 2
        t.assert_equal(2, self.counter)

    def test_second(self, t: TestContext):
        t.assert_false(self.torn_class_down)
        # teardownc(test_first): counter = counter - 1 = 1
        # setup (test_second): counter = counter + 2 = 3
        t.assert_equal(3, self.counter)

    @classmethod
    def teardown_class(cls):
        cls.torn_class_down = True


def test_class_is_torn_down(t: TestContext):
    t.assert_true(TestSetupAndTeardown.torn_class_down, "test class was not torn down :(")
