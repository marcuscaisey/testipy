from testipy import TestContext
from test_data.discovery.functions_and_classes import test_one, TestOne  # noqa: F401


def test_defined_in_this_module(t: TestContext):
    t.fail("oh no!")


class TestDefinedInThisModule:
    def test_defined_in_this_module(self, t: TestContext):
        t.fail("oh no!")
