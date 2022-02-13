from typing import Callable

from .context import TestContext, StopTest
from .results import PassResult, FailResult, ErrorResult, TestResult


TestFunction = Callable[[TestContext], None]


def _run_test_function(f: TestFunction) -> TestResult:
    t = TestContext()
    try:
        f(t)
    except StopTest:
        pass
    except Exception as e:
        return ErrorResult(f.__name__, error=e)
    if not t._passed:
        return FailResult(f.__name__, messages=t._messages)
    return PassResult(f.__name__)
