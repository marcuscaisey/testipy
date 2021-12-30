from running import TestContext
from test_data.discovery.one_valid_test import test_one


def test_defined_in_this_module(t: TestContext):
    t.fail("oh no!")
