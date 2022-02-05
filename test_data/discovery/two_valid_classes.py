from testipy import TestContext


class TestMissingTestContext:
    def test_missing_test_context(self):
        pass


class TestMissingTestFunction:
    def foo(self):
        pass


class TestOne:
    def test_one(self, t: TestContext):
        t.fail("oh no!")


class TestUntypedTestContext:
    def test_untyped_test_context(self, t):
        t.fail("oh no!")


class NoTestPrefix:
    def no_test_prefix(self, t: TestContext):
        t.fail("oh no!")


class TestTwo:
    def test_two(self, t: TestContext):
        t.fail("oh no!")
