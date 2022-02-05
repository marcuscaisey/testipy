from testipy import TestContext


def test_multiple_failures(t: TestContext):
    t.fail("failure message")
    t.fail()
    t.fail("multiple failures are allowed in the same test")


def test_require_failure(t: TestContext):
    t.fail("requiring a failure stops the test", require=True)
    t.fail("won't reach here")
