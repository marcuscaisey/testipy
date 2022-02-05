from testipy import TestContext


def raises_exception():
    raise ValueError("oh no!")


def test_exceptions_error_the_test(t: TestContext):
    raises_exception()
