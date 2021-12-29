import dataclasses
from typing import Callable, Iterable


@dataclasses.dataclass(order=False)
class TestResult:
    test_name: str
    is_pass: bool = True
    message: str = ""

    def _fail(self, message: str):
        self.is_pass = False
        self.message = message


class TestContext:
    def __init__(self, result: TestResult):
        self.result = result

    def fail(self, message: str = ""):
        self.result._fail(message)


TestFunction = Callable[[TestContext], None]


def run_tests(tests: Iterable[TestFunction]) -> list[TestResult]:
    results = []
    for test in tests:
        result = TestResult(test.__name__)
        t = TestContext(result)
        test(t)
        results.append(t.result)
    return results
