from testipy import TestContext


def test_one(t: TestContext):
    t.fail("oh no!")


def test_two(t: TestContext):
    t.fail("oh no!")


class TestOne:
    def test_a(self, t: TestContext):
        t.fail("oh no!")


class TestTwo:
    def test_b(self, t: TestContext):
        t.fail("oh no!")
