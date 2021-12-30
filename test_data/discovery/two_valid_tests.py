from running import TestContext


def test_missing_test_context():
    pass


def test_one(t: TestContext):
    t.fail("oh no!")


def test_untyped_test_context(t):
    t.fail("oh no!")


def no_test_prefix(t: TestContext):
    t.fail("oh no!")


def test_two(t: TestContext):
    t.fail("oh no!")
