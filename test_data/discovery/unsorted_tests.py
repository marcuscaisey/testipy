from testipy import TestContext


def test_b(t: TestContext):
    t.fail("oh no!")


class TestB:
    def test_b(self, t: TestContext):
        t.fail("oh no!")


def test_a(t: TestContext):
    t.fail("oh no!")


class TestA:
    def test_a(self, t: TestContext):
        t.fail("oh no!")
