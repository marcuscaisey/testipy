from running import TestContext


def test_b(t: TestContext):
    t.fail("oh no!")


def test_a(t: TestContext):
    t.fail("oh no!")
